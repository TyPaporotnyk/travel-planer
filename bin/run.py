from pathlib import Path
import sys

import uvicorn

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", reload=True)
