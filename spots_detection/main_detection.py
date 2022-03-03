import matplotlib.pyplot as plt
from spots_detection import detection_on_frame as fr_detect
import cv2
import glob

def find_empty_spots(source_path=None,id=None,isVideo=False):
    if source_path is None:
        print("Source path required!")
    elif id is None:
        print("Parking ID required!")
    else:
        try:
            if not isVideo:
                image=plt.imread(source_path)
                detect_image=fr_detect.get_available_spots(image,id)
                plt.imshow(detect_image)
                plt.show()
                cv2.imwrite('detect_image.jpg',cv2.cvtColor(detect_image, cv2.COLOR_RGB2BGR))
                return detect_image
            else:
                fwidth, fheight = 0, 0
                VIDEO_SOURCE = source_path
                video_capture = cv2.VideoCapture(VIDEO_SOURCE)
                if video_capture.isOpened():
                    success,frame=video_capture.read()
                    fshape=frame.shape
                    fheight=fshape[0]
                    fwidth=fshape[1]
                    if not success:
                        print("Video not loaded!")
                        return False
                    output_vid=cv2.VideoWriter('detect_video.mp4',-1,20.0,(fwidth,fheight))
                    while video_capture.isOpened():
                        success,frame=video_capture.read()
                        if not success:
                            break
                        rgb_image = frame[:, :, ::-1]
                        new_frame = fr_detect.get_available_spots(rgb_image, id)
                        output_vid.write(new_frame)
                        cv2.imshow('Video', new_frame)

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    video_capture.release()
                    output_vid.release()
                    cv2.destroyAllWindows()

        except FileNotFoundError:
            print("File not found!")

#   dir_path='path_to_imgs'
# for filename in glob.glob(dir_path):
#     print(filename)
#     find_empty_spots(filename,'mosgor')
find_empty_spots('path_to_img_or_video_avi','key')
