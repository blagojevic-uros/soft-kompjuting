import numpy as np
import cv2 as cv2
from matplotlib import pyplot as plt
import os
import sklearn.metrics as sklearn

left_wall_right_edge = ()
right_wall_left_edge = ()
top_wall_bottom_edge = ()

def get_walls(edges):
  global top_wall_bottom_edge
  global right_wall_left_edge
  global left_wall_right_edge

  indices = np.where(edges != [0])
  coordinates = zip(indices[0], indices[1])
  copy_coords = zip(indices[0], indices[1])
  copy_copy_coords = zip(indices[0], indices[1])
  copy_copy_copy_coords = zip(indices[0], indices[1])

  # Pravimo kontinuitet vertikalnih linija
  vertical_walls = {}
  for i in coordinates:
    if i[1] in vertical_walls.keys():
        vertical_walls[i[1]] += 1
    else:
        vertical_walls[i[1]] = 0

  # Dodajemo u listu kako bi lakse sortirali vrednosti
  vertical_filter = []
  for value in vertical_walls.values():
    vertical_filter.append(value)
  vertical_filter.sort(reverse=True)

  # Prve 4 najvece vrednosti uzimamo kao leve i desne ivice vertikalnih zidova
  # Referentna najduza ce biti prva, jer u u teoriji moze da pobegne koji piksel levo ili desno
  # Takodje na desnoj strani imamo onu ciglu, pa su nam desne ivice krace
  all_heights = [vertical_filter[0],vertical_filter[1],vertical_filter[2],vertical_filter[3]]
  height_edges = []

  # Trazimo X koordinate ovih 4 najduza zida
  for key,value in vertical_walls.items():
    for height in all_heights:
      if height == value:
        height_edges.append(key)
  height_edges.sort()
  # Sort je od levih koordinata ka desnim, tj od manjih ka vecim

  # Dodeljujemo vrednosti X koordinatama
  left_wall_top_right__x = height_edges[1]
  left_wall_bottom_right_x = left_wall_top_right__x
  find_left_y = []
  right_wall_top_left_x = height_edges[2]
  right_wall_bottom_left_x = right_wall_top_left_x

  # Copy coords koristim jer iz nekog razloga nece da udje u coordinates
  # Posto znamo X koordinatu, prolazimo kroz sve piksele koji imaju taj X
  # Uzimamo najmanji i najveci Y jer su to gornja i donja Y koordinata ivice zida
  # Proveravamo izmedju ostalog zbog slova iznad igre, da li postoji visinska razlika medju pikselima
  # Jer ako je velika razlika, nisu kontinualni i samim tim su vrv slova
  for i in copy_coords:
    if i[1] == left_wall_top_right__x:
      if len(find_left_y) == 0 or len(find_left_y) == 1:
        find_left_y.append(i[0])
      else:
        #Prethodni el mora da ima razliku sa trenutnim manju od 5 ~ neka moja procena
        if i[0] - find_left_y[len(find_left_y)-1] > 10:
          find_left_y = []
        find_left_y.append(i[0])  
  find_left_y.sort()

  left_wall_top_right_y = find_left_y[0]
  left_wall_bottom_right_y = find_left_y[len(find_left_y)-1]
  right_wall_top_left_y = left_wall_top_right_y
  right_wall_bottom_left_y = left_wall_bottom_right_y

  left_wall_right_edge = (left_wall_top_right__x+1,left_wall_top_right_y,left_wall_bottom_right_x+1,left_wall_bottom_right_y)
  right_wall_left_edge = (right_wall_top_left_x-2,right_wall_top_left_y,right_wall_bottom_left_x-2,right_wall_bottom_left_y)

  # Pravimo kontinuitet horizontalnih linija
  horisontal_walls = {}
  for i in copy_copy_coords:
    if i[0] in horisontal_walls.keys():
        horisontal_walls[i[0]] += 1
    else:
        horisontal_walls[i[0]] = 0

  # Dodajemo u listu kako bi lakse sortirali vrednosti
  horisontal_filter = []
  for value in horisontal_walls.values():
    horisontal_filter.append(value)
  horisontal_filter.sort(reverse=True)

  top_wall_length = horisontal_filter[0]
  lenght_edges = []

  # Trazimo X koordinate ovih 4 najduza zida
  for key,value in horisontal_walls.items():
    if top_wall_length == value:
      lenght_edges.append(key)
  top_wall_y = lenght_edges[1]

  x_coords = []
  for i in copy_copy_copy_coords:
    if i[0] == top_wall_y:
      x_coords.append(i[1])

  x_coords.sort()
  top_wall_left_x = x_coords[0]
  top_wall_right_x = x_coords[len(x_coords)-1]

  top_wall_bottom_edge = (top_wall_left_x,top_wall_y,top_wall_right_x,top_wall_y)

def main_func():
  global top_wall_bottom_edge
  global right_wall_left_edge
  global left_wall_right_edge
  os.system('cls')
  
  cap = cv2.VideoCapture('video1.mp4')

  collision_counter = 0

  # Check if camera opened successfully
  if (cap.isOpened()== False): 
    print("Error opening video stream or file")

  touch = 0
  counter = 0
  ball_counter = 0
  while(cap.isOpened()):
    counter += 1
    ball_counter += 1

    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
      if(counter == 1):      
        edges = cv2.Canny(frame,300,400)
        get_walls(edges)
      
      img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) 
      ret, img_bin = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
      contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
      img = frame.copy()

      for contour in contours:
        ((x, y), radius) = cv2.minEnclosingCircle(contour)
        #Po frejmu, X se poveca za 4.5 a Y za 9.5
        if radius > 4 and radius < 5:
          right_wall_x = right_wall_left_edge[0]
          left_wall_x = left_wall_right_edge[0]
          if( right_wall_x - (x+radius)) < 4 and ball_counter > 3:
            touch += 1
            print("desna")
            ball_counter = 0
          if(abs(left_wall_x - (x-radius))) < 4 and ball_counter > 3:
            touch += 1
            print("leva")
            ball_counter = 0

      plt.subplot(121),plt.imshow(frame,cmap = 'gray')
      plt.title('Original Image'), plt.xticks([]), plt.yticks([])
      plt.subplot(122),plt.imshow(img,cmap = 'gray')
      plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

      # if counter % 20 == 0:
      #     plt.show()

      # Press Q on keyboard to  exit
      if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    # Break the loop
    else: 
      break

  # When everything done, release the video capture object
  cap.release()

  # Closes all the frames
  print("ALAAAAA")
  print(touch)
  cv2.destroyAllWindows()


if __name__ == "__main__":
  main_func()