from transformers import pipeline
import fitz  # PyMuPDF
import re

class LegalAnalyzer:
    def __init__(self):
        print("Initializing Professional Audit Engine...")
        # zero-shot for category risk mapping
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def extract_pdf_text(self, file_bytes):
        """Robust PDF extraction for large documents."""
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            return f"PDF Error: {str(e)}"

    def analyze_text(self, text):
        categories = ["Liability Limitation", "Data Privacy", "Forced Arbitration", "Termination Rights"]
        # Analyze first 1024 chars for high-level classification
        results = self.classifier(text[:1024], categories, multi_label=True)
        
        findings = []
        for label, score in zip(results['labels'], results['scores']):
            if score > 0.45:
                risk = "High" if score > 0.75 else "Medium"
                findings.append({
                    "category": label,
                    "risk": risk,
                    "confidence": int(score * 100),
                    "text": self._get_legal_context(label)
                })
        return findings

    def _get_legal_context(self, label):
        context = {
            "Liability Limitation": "Contractual cap on damages recoverable by the user for errors.",
            "Data Privacy": "Provisions governing the harvest and third-party sale of personal identifiers.",
            "Forced Arbitration": "Requirement to waive jury trial in favor of private, binding settlement.",
            "Termination Rights": "Provisions allowing account suspension or deletion without prior notice."
        }
        return context.get(label, "Standard legal provision.")

    def get_evidence(self, text):
        """Extracts specific, quoted sentences for reasoning."""
        triggers = {
            "ARBITRATION": ["arbitration", "waive", "binding", "class action"],
            "LIABILITY": ["not liable", "limitation of liability", "indemnify", "disclaim"],
            "PRIVACY": ["collect", "third party", "sharing", "cookies", "track"],
            "TERMINATION": ["at our discretion", "without notice", "terminate", "suspend"]
        }
        evidence = []
        # Split text into clean sentences
        sentences = re.split(r'(?<=[.!?]) +', text.replace('\n', ' '))
        
        found_cats = set()
        for sentence in sentences:
            if len(evidence) >= 4: break
            s_lower = sentence.lower()
            for cat, keywords in triggers.items():
                if cat not in found_cats and any(kw in s_lower for kw in keywords):
                    clean_s = sentence.strip()
                    if 30 < len(clean_s) < 250: # Filter for 'quote-worthy' snippets
                        evidence.append({"type": cat, "quote": clean_s})
                        found_cats.add(cat)
                        break
        return evidence