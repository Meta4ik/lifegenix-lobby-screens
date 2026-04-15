import os
from playwright.sync_api import sync_playwright

def capture_slides():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        
        # Get absolute path to index.html
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = f"file://{os.path.join(base_dir, 'index.html')}"
        
        print(f"Loading {file_path}...")
        page.goto(file_path)
        
        # Wait for automation hooks to be ready
        page.wait_for_function("window.getSlideCount !== undefined")
        
        slide_count = page.evaluate("window.getSlideCount()")
        print(f"Detected {slide_count} slides. Starting capture...")
        
        output_dir = os.path.join(base_dir, "slide_exports_py")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        for i in range(slide_count):
            # Navigate to slide
            page.evaluate(f"window.gotoSlide({i})")
            
            # Brief pause for transitions
            page.wait_for_timeout(500)
            
            # Get title for filename
            title = page.evaluate("window.getSlideTitle()")
            clean_title = "".join([c if c.isalnum() else "_" for c in title])
            filename = f"{str(i+1).zfill(2)}_{clean_title}.png"
            
            # Take screenshot
            save_path = os.path.join(output_dir, filename)
            page.screenshot(path=save_path)
            print(f"Captured Slide {i+1}/{slide_count}: {filename}")
            
        browser.close()
        print(f"Done! All slides exported to {output_dir}")

if __name__ == "__main__":
    # Note: Requires 'pip install playwright' and 'playwright install chromium'
    try:
        capture_slides()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to install dependencies:")
        print("  pip install playwright")
        print("  playwright install chromium")
