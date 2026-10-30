"""
NodeCrawler: A utility class for scraping V2Ray subscription links
from specific web sources (yudou789 and mibei77) and downloading them.
"""

import requests
import re
import os
import base64
from typing import List, Tuple, Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time

# --- Configuration Constants ---
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
YUDOU_BASE_URL = "https://www.yudou789.top/"
MIBEI_BASE_URL = "https://www.mibei77.com/category/jiedian"
TIMEOUT_SECONDS = 10
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE64_OUTPUT_FILE = os.path.join(SCRIPT_DIR, "base64")

# --- Type Definitions ---
# Define a clear type alias for the result structure
# (Node Title, V2Ray/plain .txt URL, Clash Meta .yaml URL or None)
# NOTE: legacy 2-tuples (title, txt_url) are still accepted by process_results.
SubscriptionResult = Tuple[str, str, Optional[str]]

def clean_existing_nodes(output_directory: str) -> List[str]:
    """
    Deletes all existing subscription files (.txt and .yaml/.yml) within the
    specified output directory.

    Args:
        output_directory: The directory to clean.

    Returns:
        A list of filenames that were successfully deleted.
    """
    deleted_files: List[str] = []
    if not os.path.isdir(output_directory):
        print(f"Directory does not exist: {output_directory}")
        return deleted_files

    print(f"--- Starting cleanup in: {output_directory} ---")

    # Both the plain .txt subscriptions and the Clash Meta .yaml subscriptions
    # are produced by this crawler, so both must be cleared before a fresh run.
    cleanup_extensions = (".txt", ".yaml", ".yml")

    for filename in os.listdir(output_directory):
        if filename.endswith(cleanup_extensions):
            filepath = os.path.join(output_directory, filename)
            try:
                os.remove(filepath)
                print(f"✓ Deleted file: {filename}")
                deleted_files.append(filename)
            except OSError as e:
                print(f"✗ Error deleting file {filename}: {e}")

    print("--- Cleanup complete ---")
    return deleted_files


NODE_LINK_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.\-]*://')

def extract_node_lines(content: str) -> List[str]:
    """
    Returns the plain node links (one per line) carried by a subscription body.

    Downloaded `.txt` subscriptions are usually a single base64 blob, but some
    sources serve the links already in plain text, so both shapes are accepted.
    """
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if lines and all(NODE_LINK_RE.match(line) for line in lines):
        return lines

    try:
        decoded = base64.b64decode(''.join(lines), validate=True).decode('utf-8')
    except (ValueError, UnicodeDecodeError):
        return lines

    return [line.strip() for line in decoded.splitlines() if line.strip()]

def write_base64_subscription(output_directory: str = 'nodes_output',
                              target_path: str = BASE64_OUTPUT_FILE) -> Optional[str]:
    """
    Merges every `.txt` subscription in the output directory into one
    base64-encoded blob and writes it to the repository root ``base64`` file.

    Args:
        output_directory: Directory holding the downloaded ``.txt`` subscriptions.
        target_path: Destination file for the merged base64 subscription.

    Returns:
        The ``target_path`` on success, or ``None`` when there were no nodes.
    """
    if not os.path.isdir(output_directory):
        print(f"Directory does not exist: {output_directory}")
        return None

    txt_files = sorted(
        os.path.join(output_directory, name)
        for name in os.listdir(output_directory)
        if name.endswith('.txt')
    )

    node_lines: List[str] = []
    seen = set()

    for filepath in txt_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except IOError as e:
            print(f"✗ Failed to read {filepath}: {e}")
            continue

        before = len(node_lines)
        for line in extract_node_lines(content):
            if line not in seen:
                seen.add(line)
                node_lines.append(line)
        print(f"✓ {os.path.basename(filepath)}: {len(node_lines) - before} new nodes")

    if not node_lines:
        print("✗ No nodes found, base64 subscription was not updated.")
        return None

    encoded = base64.b64encode('\n'.join(node_lines).encode('utf-8')).decode('ascii')
    try:
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(encoded)
    except IOError as e:
        print(f"✗ Failed to write {target_path}: {e}")
        return None

    print(f"\n✅ Base64 subscription saved: {target_path} "
          f"({len(node_lines)} nodes from {len(txt_files)} files)")
    return target_path


class NodeCrawler:
    """
    Manages the crawling, link extraction, and downloading of V2Ray 
    subscription links from various web sources.
    """
    def __init__(self, output_directory: str = 'nodes_output'):
        """
        Initializes the NodeCrawler.

        Args:
            output_directory: The local directory where subscription files will be saved.
        """
        self.output_directory = output_directory
        self._setup_output_directory()
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    def _setup_output_directory(self) -> None:
        """Ensures the output directory exists."""
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def _fetch_page_content(self, url: str) -> Optional[str]:
        """
        Fetches the raw text content of a given URL with a timeout.

        Args:
            url: The URL to fetch.

        Returns:
            The page content as a string, or None if fetching fails.
        """
        try:
            response = self.session.get(url, timeout=TIMEOUT_SECONDS)
            response.encoding = 'utf-8'
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page {url}: {type(e).__name__} - {e}")
            return None

    def _save_content(self, filename: str, content: str) -> bool:
        """
        Saves content to a file in the output directory.

        Args:
            filename: The desired filename (e.g., 'site_1_NodeTitle_v2ray.txt').
            content: The text content to write.

        Returns:
            True if saving was successful, False otherwise.
        """
        filepath = os.path.join(self.output_directory, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Saved: {filepath}")
            return True
        except IOError as e:
            print(f"✗ File save error for {filename}: {e}")
            return False

    def _is_relevant_link(self, link: str) -> bool:
        """
        Filters out irrelevant links and keeps only subscription files that
        belong to the supported sources (or are explicitly v2ray links).
        """
        low = link.lower()
        if 'v2ray' in low:
            return True
        return any(token in low for token in ('yudou', 'mibei', 'mm.'))

    def _extract_subscription_links(
        self, content_text: str, site_name: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts BOTH subscription links from raw page content:
          * the plain `.txt` link   (V2Ray / 小火箭 / winxray / Clash-agnostic)
          * the Clash Meta `.yaml` link

        The source pages often render the two links inside a single text node
        with NO whitespace between them, e.g.::

            "https://hh.yudou226.top/.../xxx.txtClash Meta订阅链接...https://hh.yudou226.top/.../yyy.yaml"

        A naive ``https://\\S+\\.yaml`` regex would start at the first URL and
        swallow everything up to ``.yaml``, producing one garbage link. We avoid
        this by inserting a line break before every ``http`` occurrence first, so
        each URL sits on its own line and is matched independently.

        Args:
            content_text: The full text content of the page.
            site_name: The name of the site, used only for logging.

        Returns:
            A ``(txt_url, yaml_url)`` tuple; each element is ``None`` if not found.
        """
        # 1) Normalize: give every URL its own line so adjacent links never merge.
        normalized = re.sub(r'(?=https?://)', '\n', content_text)

        txt_url: Optional[str] = None
        yaml_url: Optional[str] = None

        for raw_line in normalized.splitlines():
            line = raw_line.strip()
            if not line.startswith('http'):
                continue

            # Non-greedy so we stop at the FIRST matching extension on this line.
            txt_match = re.match(r'(https?://\S*?\.txt)', line)
            yaml_match = re.match(r'(https?://\S*?\.ya?ml)', line)

            if txt_match and txt_url is None:
                candidate = txt_match.group(1)
                if self._is_relevant_link(candidate):
                    txt_url = candidate

            elif yaml_match and yaml_url is None:
                candidate = yaml_match.group(1)
                if self._is_relevant_link(candidate):
                    yaml_url = candidate

            if txt_url and yaml_url:
                break

        if not txt_url:
            print(f"    ✗ No .txt subscription link found ({site_name}).")
        if not yaml_url:
            print(f"    ✗ No .yaml subscription link found ({site_name}).")

        return txt_url, yaml_url

    def _extract_v2ray_links(self, content_text: str, site_name: str) -> Optional[str]:
        """
        Backward-compatible accessor: returns only the plain `.txt` link.

        Kept for any external callers; internally it now delegates to
        :meth:`_extract_subscription_links` so the two stay consistent.
        """
        txt_url, _ = self._extract_subscription_links(content_text, site_name)
        return txt_url

    def crawl_yudou789(self, limit: int = 2) -> List[SubscriptionResult]:
        """Crawls yudou789.top, extracts links, and processes results."""
        print("\n" + "="*50)
        print(f"Starting crawl for yudou789.top (Limit: {limit})")
        print("="*50)

        html = self._fetch_page_content(YUDOU_BASE_URL)
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all(class_='item-heading')
        results: List[SubscriptionResult] = []

        print(f"Found {len(items)} node listings.")

        nodes_to_process = items[:limit]

        for idx, item in enumerate(nodes_to_process, 1):
            a_tag = item.find('a')
            if not a_tag or not a_tag.get('href'):
                continue

            title = a_tag.get_text(strip=True)
            share_url = urljoin(YUDOU_BASE_URL, a_tag['href'])

            print(f"\n[{idx}] Title: {title}")
            print(f"    Visit: {share_url}")

            share_html = self._fetch_page_content(share_url)
            if not share_html:
                continue

            soup_share = BeautifulSoup(share_html, 'html.parser')
            hidden_content_tag = soup_share.find(class_='cl-hidden-content')

            content_text: Optional[str] = None

            if hidden_content_tag:
                # Logic: Latest two nodes (idx <= 2) require explicit extraction logic
                is_latest_two = (idx <= 2)

                if is_latest_two:
                    print("    [Unlock Required] Extracting hidden content...")
                else:
                    # Non-latest nodes: assume link is in public content
                    print("    [Direct Extract] Extracting links from public content...")
                content_text = hidden_content_tag.get_text(strip=True)
            else:
                print("    [No Hidden Content] Extracting links from main content...")
                content_text = soup_share.get_text(strip=True)

            # Extract BOTH the plain .txt link and the Clash Meta .yaml link.
            v2ray_url, yaml_url = self._extract_subscription_links(content_text, 'yudou789')

            if v2ray_url:
                print(f"    Found V2Ray URL: {v2ray_url}")
            else:
                print("    ✗ V2Ray link not found in the content.")

            if yaml_url:
                print(f"    Found Clash YAML URL: {yaml_url}")

            # Keep every successfully extracted link (txt and/or yaml).
            if v2ray_url or yaml_url:
                results.append((title, v2ray_url or '', yaml_url))

            time.sleep(1)

        return results

    def crawl_mibei77(self, limit: int = 2) -> List[SubscriptionResult]:
        """Crawls mibei77.com, extracts links, and processes results."""
        print("\n" + "="*50)
        print("Starting crawl for mibei77.com")
        print("="*50)

        html = self._fetch_page_content(MIBEI_BASE_URL)
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all(class_='item-heading')
        results: List[SubscriptionResult] = []

        print(f"Found {len(items)} node listings.")

        for idx, item in enumerate(items[:limit], 1):
            a_tag = item.find('a')
            if not a_tag or not a_tag.get('href'):
                continue

            title = a_tag.get_text(strip=True)
            share_url = urljoin(MIBEI_BASE_URL, a_tag['href'])

            print(f"\n[{idx}] Title: {title}")
            print(f"    Visit: {share_url}")

            share_html = self._fetch_page_content(share_url)
            if not share_html:
                continue

            soup_share = BeautifulSoup(share_html, 'html.parser')
            content_box = soup_share.find(class_='theme-box wp-posts-content')

            if content_box:
                content_text = content_box.get_text(strip=True)

                # Extract BOTH the plain .txt link and the Clash Meta .yaml link.
                v2ray_url, yaml_url = self._extract_subscription_links(content_text, 'mibei77')

                if v2ray_url:
                    print(f"    Found V2Ray URL: {v2ray_url}")
                else:
                    print("    ✗ V2Ray link not found in the content.")

                if yaml_url:
                    print(f"    Found Clash YAML URL: {yaml_url}")

                if v2ray_url or yaml_url:
                    results.append((title, v2ray_url or '', yaml_url))
            else:
                print("    ✗ Content box not found.")

            time.sleep(1)

        return results

    def process_results(self, results: List[SubscriptionResult], site_name: str) -> None:
        """
        Processes the raw results by downloading the subscription file(s) for
        each node: the plain `.txt` link and, when available, the Clash Meta
        `.yaml` link.

        Backward compatible: accepts both legacy ``(title, txt_url)`` tuples and
        the extended ``(title, txt_url, yaml_url)`` tuples.

        Args:
            results: A list of result tuples returned by the crawler.
            site_name: The name of the site to use in the final filenames.
        """
        if not results:
            print(f"\n✗ No results obtained from {site_name}.")
            return

        print(f"\nStarting download process for {site_name} ({len(results)} nodes)...")
        print("-" * 50)

        for idx, entry in enumerate(results, 1):
            # Backward-compatible unpack: 2-tuple (legacy) or 3-tuple (with yaml).
            title = entry[0]
            txt_url: Optional[str] = entry[1] or None
            yaml_url: Optional[str] = entry[2] if len(entry) > 2 else None

            # Self-Documenting Naming: Clean the title for file system safety
            safe_title = re.sub(r'[^\w\u4e00-\u9fff-]', '_', title)[:50]

            print(f"\n[{idx}] Downloading: {title}")

            # --- 1) Plain .txt subscription (V2Ray / 小火箭 / winxray / Clash 通用) ---
            if txt_url:
                txt_filename = f"{site_name}_{idx}_{safe_title}_v2ray.txt"
                print(f"    Source (txt):  {txt_url}")
                self._download_subscription(txt_url, txt_filename)
            else:
                print("    ✗ Skipped: no .txt subscription link.")

            # --- 2) Clash Meta subscription (.yaml) ---
            if yaml_url:
                yaml_filename = f"{site_name}_{idx}_{safe_title}_clash.yaml"
                print(f"    Source (yaml): {yaml_url}")
                self._download_subscription(yaml_url, yaml_filename)
            else:
                print("    ✗ Skipped: no .yaml subscription link.")

            time.sleep(0.5)

    def _download_subscription(self, url: str, filename: str) -> bool:
        """Handles the download operation for a single subscription link."""
        try:
            response = self.session.get(url, timeout=TIMEOUT_SECONDS)
            response.encoding = 'utf-8'
            # Use the save method for consistency
            success = self._save_content(filename, response.text)
            return success
        except requests.RequestException as e:
            print(f"✗ Download failed for {url} ({filename}): {type(e).__name__}")
            return False

    def run(self, limit: int = 2) -> None:
        """
        Executes the full crawling workflow.

        Args:
            limit: The number of latest nodes to crawl from each site.
        """
        print("\n🚀 Node Crawler Execution Start")
        print(f"Output Directory: {os.path.abspath(self.output_directory)}")

        # 1. Crawl and Process Yudou789
        yudou_results = self.crawl_yudou789(limit=limit)
        self.process_results(yudou_results, 'yudou789')

        # 2. Crawl and Process Mibei77
        mibei_results = self.crawl_mibei77(limit=limit)
        self.process_results(mibei_results, 'mibei77')

        # 3. Merge the downloaded .txt subscriptions into the root base64 file.
        write_base64_subscription(self.output_directory)

        print("\n" + "="*50)
        print("✅ Crawler Execution Complete")
        print("="*50)


if __name__ == '__main__':
    """
    Main execution block for the NodeCrawler script.
    """
    try:
        crawler = NodeCrawler()
        clean_existing_nodes(crawler.output_directory)
        crawler.run(limit=2)
    except KeyboardInterrupt:
        print("\n\n⚠ User interrupted the process.")
    except Exception as e:
        print(f"\n✗ Critical Error during execution: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
