# gesture-controlled-mouse-pointer
Control your mouse pointer without your fingers touching your mouse/touchpad !

It uses a webcam to capture the video feed and a python script (with libraries - OpenCV and pyautogui) to process the feed, track your finger movements and emulate the mouse pointer accordingly. 

The setup requires 
1. Two same colored strips across your index finger and thumb.
2. Calliberate the mask(using trackbars provided) till the strips are the only thing visible on the feed.

Once setted up..
Here's how to use
1. Move the fingers with a gap between them to move pointer.
2. Tap the fingers togather to emulate a left-click.
3. Tap and hold (without moving your hand) to emulate right-click.
4. Tap and drag to select or emulate drag action.
