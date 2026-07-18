import json
import logging
import urllib.error
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)


class OllamaClientError(Exception):
    """Controlled error raised when an Ollama API request fails."""


class OllamaClient:
    """HTTP client for Ollama chat completions.

    Accepts a single final prompt string. Tries the OpenAI-compatible
    endpoint first, then falls back to the native Ollama chat API.
    """

    def __init__(self):
        self.base_url = (
            getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
            or 'http://localhost:11434'
        ).rstrip('/')
        self.model = getattr(settings, 'OLLAMA_MODEL', 'qwen2.5-coder:3b') or 'qwen2.5-coder:3b'
        self.timeout = int(getattr(settings, 'OLLAMA_TIMEOUT', 120))

    def review(self, prompt):
        """Send one final prompt to Ollama and return the raw text response."""
        if not prompt or not str(prompt).strip():
            raise OllamaClientError('Prompt must not be empty')

        messages = [
            {
                'role': 'user',
                'content': str(prompt),
            }
        ]

        try:
            return self._review_openai_compatible(messages)
        except _OllamaEndpointUnavailable as exc:
            logger.info(
                'Ollama OpenAI-compatible endpoint unavailable (%s); '
                'falling back to native /api/chat',
                exc,
            )
            try:
                return self._review_native(messages)
            except OllamaClientError:
                raise
            except Exception as native_exc:
                logger.warning('Unexpected Ollama native client error: %s', native_exc)
                raise OllamaClientError(str(native_exc)) from native_exc
        except OllamaClientError:
            raise
        except Exception as exc:
            logger.warning('Unexpected Ollama client error: %s', exc)
            raise OllamaClientError(str(exc)) from exc

    def _review_openai_compatible(self, messages):
        url = f'{self.base_url}/v1/chat/completions'
        payload = {
            'model': self.model,
            'messages': messages,
        }
        body = self._post_json(url, payload, allow_fallback_on_http=(404, 405))
        return self._extract_openai_content(body)

    def _review_native(self, messages):
        url = f'{self.base_url}/api/chat'
        payload = {
            'model': self.model,
            'messages': messages,
            'stream': False,
        }
        body = self._post_json(url, payload)
        return self._extract_native_content(body)

    def _post_json(self, url, payload, allow_fallback_on_http=()):
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST',
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='replace')
            if allow_fallback_on_http and exc.code in allow_fallback_on_http:
                raise _OllamaEndpointUnavailable(
                    f'HTTP {exc.code} from {url}'
                ) from exc
            logger.warning('Ollama HTTP error %s: %s', exc.code, detail)
            raise OllamaClientError(f'Ollama API returned HTTP {exc.code}') from exc
        except urllib.error.URLError as exc:
            logger.warning('Ollama connection error: %s', exc)
            raise OllamaClientError('Ollama API connection failed') from exc
        except TimeoutError as exc:
            logger.warning('Ollama request timed out')
            raise OllamaClientError('Ollama API request timed out') from exc
        except json.JSONDecodeError as exc:
            logger.warning('Ollama returned invalid JSON')
            raise OllamaClientError('Ollama API returned invalid JSON') from exc

    def _extract_openai_content(self, body):
        choices = body.get('choices') or []
        if not choices:
            raise _OllamaEndpointUnavailable('OpenAI-compatible response has no choices')

        message = choices[0].get('message') or {}
        content = message.get('content')
        if content is None:
            raise OllamaClientError('Ollama API returned empty content')

        return content

    def _extract_native_content(self, body):
        message = body.get('message') or {}
        content = message.get('content')
        if content is None:
            raise OllamaClientError('Ollama API returned empty content')

        return content


class _OllamaEndpointUnavailable(Exception):
    """Internal signal to fall back from OpenAI-compatible to native API."""
