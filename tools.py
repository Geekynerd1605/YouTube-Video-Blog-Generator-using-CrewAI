# pytube often breaks when YouTube changes; crewai_tools uses it for channel loading.
import sys

try:
    import pytubefix as _pytubefix

    sys.modules["pytube"] = _pytubefix
except ImportError:
    _pytubefix = None


def _patch_pytubefix_channel_url_generator() -> None:
    """pytubefix Channel.url_generator yields YouTube/Playlist objects; crewai_tools expects str URLs."""
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
    """Turn @handle or handle into a full channel URL RagTool/pytube accept."""
    s = handle_or_url.strip()
    if s.startswith("http://") or s.startswith("https://"):
        return s
    handle = s[1:] if s.startswith("@") else s
    return f"https://www.youtube.com/@{handle}"


class YoutubeChannelSearchToolFixed(YoutubeChannelSearchTool):
    """Work around crewai_tools prepending '@' to full URLs, which breaks urlparse and file-path checks."""

    def add(self, youtube_channel_handle: str) -> None:
        url = _normalize_channel_url(youtube_channel_handle)
        RagTool.add(self, url, data_type=DataType.YOUTUBE_CHANNEL)


# Use handle only; do not pass a bare https URL through YoutubeChannelSearchTool.add() — it becomes @https://...
# Default 0.6 similarity is strict; channel RAG often needs a lower bar to return chunks.
yt_tool = YoutubeChannelSearchToolFixed(
    youtube_channel_handle="@krishnaik06",
    similarity_threshold=0.28,
    limit=12,
)
