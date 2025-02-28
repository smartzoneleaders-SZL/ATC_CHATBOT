def format_source_documents(source_docs):
    """Format source documents into a clickable link using direct URLs"""
    if not source_docs or len(source_docs) == 0:
        return ""
    
    # Define mapping between filenames and their URLs
    file_url_mapping = {
        "ATCMarket Free Membership Agreement.pdf": "https://pub-2bae66d5e6d74bfda26d9e7d8ee03534.r2.dev/documents/ATCMarket%20Free%20Membership%20Agreement.pdf",
        "ATCMarket Privacy Policy.pdf": "https://pub-2bae66d5e6d74bfda26d9e7d8ee03534.r2.dev/documents/ATCMarket%20Privacy%20Policy.pdf",
        "ATCMarket Terms of Use.pdf": "https://pub-2bae66d5e6d74bfda26d9e7d8ee03534.r2.dev/documents/ATCMarket%20Terms%20of%20Use.pdf",
        "product listing policy.pdf": "https://pub-2bae66d5e6d74bfda26d9e7d8ee03534.r2.dev/documents/product%20listing%20policy.pdf",
        "How to start selling on ATCMarket.pdf": "https://pub-2bae66d5e6d74bfda26d9e7d8ee03534.r2.dev/documents/How%20to%20start%20selling%20on%20ATCMarket.pdf",
        "Start selling on ATCMarket.pdf": "https://pub-2bae66d5e6d74bfda26d9e7d8ee03534.r2.dev/documents/How%20to%20start%20selling%20on%20ATCMarket.pdf",
        "Trade Service.pdf": "https://pub-2bae66d5e6d74bfda26d9e7d8ee03534.r2.dev/documents/Trade%20Service.pdf",
        "transaction Service agreement.pdf": "https://pub-2bae66d5e6d74bfda26d9e7d8ee03534.r2.dev/documents/transaction%20Service%20agreement.pdf"
    }
    
    # Get the most relevant source (first one)
    doc = source_docs[0]
    
    if hasattr(doc, 'metadata') and 'source' in doc.metadata:
        # Extract only the filename without the path
        full_path = doc.metadata['source']
        filename = full_path.split('\\')[-1]
        
        # Check if the filename is in our mapping
        if filename in file_url_mapping:
            url = file_url_mapping[filename]
            return f'Read More Here: <a href="{url}" target="_blank">{filename}</a>'
        else:
            # Fallback for unknown files - using the base URL with the filename
            base_url = "https://pub-2bae66d5e6d74bfda26d9e7d8ee03534.r2.dev/documents/"
            encoded_filename = filename.replace(" ", "%20")
            return f'Read More Here: <a href="{base_url}{encoded_filename}" target="_blank">{filename}</a>'
    
    return ""
    
def should_show_sources(response):
    """
    Determine if sources should be shown based on the response content
    """
    import re
    
    greeting_patterns = [
        "@atcmarket.com",
        r"\bhey\b", r"\bhi\b", r"\bhello\b", 
        r"\bbye\b", r"\bgoodbye\b", r"\bthanks\b", r"\bthank you\b",
        r"\bgood morning\b", r"\bgood afternoon\b", r"\bgood evening\b", r"\bgood night\b",
        r"\bhow can i assist you\b", r"\bI'm happy to help you\b", r"\bI'm not aware of\b"
    ]
    
    response_lower = response.lower()
    
    for pattern in greeting_patterns:
        if pattern == "@atcmarket.com" and pattern in response_lower:
            return False
        elif pattern.startswith(r"\b") and re.search(pattern, response_lower):
            return False
    
    return True
