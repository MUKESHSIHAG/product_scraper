from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .scraper import Scraper
from .settings import settings

app = FastAPI()

security = HTTPBearer()

def get_current_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != settings.static_token:
        raise HTTPException(status_code=403, detail="Invalid token")
    return credentials.credentials

@app.post("/scrape")
async def scrape(page_limit: int = settings.page_limit, proxy: str = settings.proxy, token: str = Depends(get_current_token)):
    scraper = Scraper(page_limit=page_limit, proxy=proxy)
    await scraper.scrape()
    return {"message": f"Scraped {len(scraper.products)} products."}
