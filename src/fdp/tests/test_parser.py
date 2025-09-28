from src.fdp.etl.parser import parse_pdf

def test_parse_pdf_minimal():
    out = parse_pdf("fixtures/eo/sample.pdf")
    assert set(["eo_number","title","signed_date","body_text"]).issubset(out.keys())
