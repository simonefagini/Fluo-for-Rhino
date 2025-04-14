import rhinoscriptsyntax as rs
import System.Windows.Forms as wf

def check_clipboard_formats():
    formats = wf.Clipboard.GetDataObject().GetFormats()
    
    found_image = False
    found_text = False

    for fmt in formats:
        if fmt == "Bitmap" and not found_image:
            print("Clipboard contains an image")
            found_image = True  # Prevent duplicate messages
        
        elif fmt == "Text" and not found_text:
            print("Clipboard contains text")
            found_text = True  # Prevent duplicate messages

def paste_at_point():
    """Attempts to paste Rhino objects at a user-specified point. 
    If no objects are found, checks clipboard contents."""
    
    # Step 1: Paste objects
    rs.Command("_Paste", True)
    pasted_objs = rs.LastCreatedObjects()

    # Step 2: Check if any objects were pasted
    if not pasted_objs:
        print("No Rhino objects detected in clipboard. Checking other formats...")
        check_clipboard_formats()
        return
    
    try:
        # Step 3: Get bounding box
        
        bbox = rs.BoundingBox(pasted_objs)zs 
        if not bbox:
            raise ValueError("Bounding box could not be determined.")
            
        min_point = bbox[0]
        max_point = bbox[6]  # Opposite corner
        base_point = [(min_point[0] + max_point[0])/2, (min_point[1] + max_point[1])/2, (min_point[2] + max_point[2])/2]
        
        # Step 4: Ask user forzs 
        target_point = rs.GetPoint("Pick first point")
        if target_point == None:
            return
        
        # Step 5: Move pasted objects
        translation = rs.VectorCreate(target_point, base_point) 
        rs.MoveObjects(pasted_objs, translation)
        print("Objects pasted.")

    except Exception as e:
        print("An error occurred")
        check_clipboard_formats()

# Run the function
paste_at_point()
