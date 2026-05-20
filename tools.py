"""
YouTube channel search tool and compatibility patches for crewai_tools.

- Aliases pytubefix as pytube (crewai_tools expects the pytube module name).
- Fixes Channel.url_generator to yield string watch URLs for RAG indexing.
- YoutubeChannelSearchToolFixed normalizes @handles vs full URLs for RagTool.
"""

import sys

# crewai_tools imports "pytube"; redirect to pytubefix when available (more reliable).
try:
    import pytubefix as _pytubefix

    sys.modules["pytube"] = _pytubefix
except ImportError:
    _pytubefix = None


def _patch_pytubefix_channel_url_generator() -> None:
    """Make Channel.url_generator yield str watch URLs; crewai_tools RAG expects strings, not YouTube objects."""
    if _pytubefix is None:
        return
    try:
        from pytubefix import Playlist, YouTube
        from pytubefix.contrib import channel as channel_mod
    except ImportError:
        return

    def url_generator_fixed(self):
        for page in self._paginate(self.html):
            for obj in page:
                if isinstance(obj, str):
                    yield obj
                elif isinstance(obj, YouTube):
                    yield obj.watch_url
                elif isinstance(obj, Playlist):
                    continue
                else:
                    w = getattr(obj, "watch_url", None)
                    if isinstance(w, str):
                        yield w

    channel_mod.Channel.url_generator = url_generator_fixed


_patch_pytubefix_channel_url_generator()

from crewai_tools import YoutubeChannelSearchTool
from crewai_tools.rag.data_types import DataType
from crewai_tools.tools.rag.rag_tool import RagTool


def _normalize_channel_url(handle_or_url: str) -> str:
    """Turn @handle or bare handle into https://www.youtube.com/@handle for RagTool."""
    s = handle_or_url.strip()
    if s.startswith("http://") or s.startswith("https://"):
        return s
    handle = s[1:] if s.startswith("@") else s
    return f"https://www.youtube.com/@{handle}"


class YoutubeChannelSearchToolFixed(YoutubeChannelSearchTool):
    """Avoid crewai_tools prepending '@' to full URLs, which breaks urlparse and path checks."""

    def add(self, youtube_channel_handle: str) -> None:
        url = _normalize_channel_url(youtube_channel_handle)
        RagTool.add(self, url, data_type=DataType.YOUTUBE_CHANNEL)


# Default channel and RAG tuning — adjust handle, similarity_threshold, or limit as needed.
# Use @handle form; bare https URLs in add() get mangled to @https://... by the base tool.
# similarity_threshold 0.28 is looser than default 0.6 so channel chunks match more often.
yt_tool = YoutubeChannelSearchToolFixed(
    youtube_channel_handle="@krishnaik06",
    similarity_threshold=0.28,
    limit=12,
)
