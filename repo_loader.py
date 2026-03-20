
from git import Repo
import os
import shutil
from langchain_core.documents import Document
import uuid


def load_repo(repo_url):

    # Unique folder name
    repo_path = f"repo_{uuid.uuid4().hex[:6]}"

    # Clone repo
    Repo.clone_from(repo_url, repo_path, depth=1)

    documents = []

    try:
        max_files = 120   # 🔥 limit files
        count = 0
        for root, dirs, files in os.walk(repo_path):

            # Skip .git folder
            if ".git" in root:
                continue

            for file in files:

                # Only Python files
                if file.endswith(".py") :

                    path = os.path.join(root, file)
                    if "test" in path.lower(): continue
                    if count >= max_files:
                        break

                    # Skip large files (>200KB)
                    try:
                        if os.path.getsize(path) > 200000:
                            continue
                    except:
                        continue

                    # Read file safely
                    try:
                        with open(path, "r", encoding="utf-8", errors="ignore") as f:

                            documents.append(
                                Document(
                                    page_content=f.read(),
                                    metadata={
                                        "source": path.replace(repo_path, "")
                                    }
                                )
                            )
                            count += 1
                    except:
                        continue
            if count >= max_files:
                 break

    finally:
        # Clean up (VERY IMPORTANT)
        shutil.rmtree(repo_path, ignore_errors=True)

    return documents

