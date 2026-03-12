import uvicorn
from fastapi import FastAPI, Form, UploadFile, File
from analyzer import LegalAnalyzer
from utils import scrape_url

app = FastAPI()
analyzer = LegalAnalyzer()

@app.post("/analyze")
async def process_audit(
    source_type: str = Form(...), 
    content: str = Form(None),
    file: UploadFile = File(None)
):
    text = ""
    source = source_type.lower()

    if "url" in source:
        text = scrape_url(content)
        if not text or len(text) < 200:
            return {"error": "The URL could not be audited. The site may be blocking access or contains no visible legal text."}
    
    elif "pdf" in source and file:
        file_bytes = await file.read()
        text = analyzer.extract_pdf_text(file_bytes)
        if "PDF Error" in text:
            return {"error": text}
    
    else:
        text = content if content else ""

    if not text:
        return {"error": "No content provided for neural audit."}

    # Execute Audit
    findings = analyzer.analyze_text(text)
    evidence = analyzer.get_evidence(text)

    # Calculate Score
    score = 100
    for f in findings:
        score -= 15 if f['risk'] == "High" else 7
    score -= (len(evidence) * 2) # Extra deduction for found 'smoking guns'
    
    return {
        "score": max(score, 12),
        "findings": findings,
        "evidence": evidence
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)