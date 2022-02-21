import os
import formats


#Begin by uncommenting the next two lines and custom defining the Path_name and duplicate_folder_path variables.


Path_name=    #os.getcwd() eg  'C:\Users\begin_folder'                  folder full path location to begin cleaning
duplicate_folder_path =    #-------    eg'C:\\Users\\move_duplicates_to'   #folder to contain duplicate file's full path location


count = 0  #original number of movies in your root dir(Path_name)
count2 = 0 #suspected duplicate movies by file name
count3 = 0 #suspected duplicate movies by file size
count4 = 0  #Number of movies Unreadable

moved_movies = []
movie_dict = {}

fhand = open(f"{duplicate_folder_path}\\duplicate_movie_by_name.txt", "w")

fhand.write("""\t\t\t\t\t This is a List of Suspected Duplicate Movies by Name      
                    \n \t\t\t\t\t\t\t(Ie, They Both Have the Same Name) \n """)       #Creates a text file to contain suspected movies

f2hand = open(f"{duplicate_folder_path}\\duplicate_movie_by_size.txt", "w")

f2hand.write(""""\t\t\t\t\t This is a List of Suspected Duplicate Movies by Size
                  \n \t\t\t\t\t\t\t(Ie, They Both Have the Same Size) \n """)
                  
def get_file_name(f_size):
  """
  Returns file name whose filesize correstponds with the files size passed in as parameter.
  """
    for x,(z,y) in movie_dict.items():
        if z == f_size :
            return x

        
video_formats = formats.video_formats



for path, directories, files in os.walk(Path_name):
    for file in files:
        if file.endswith(video_formats):
                              
            
            try:
                file_size = os.path.getsize(os.path.join(path,file)) 
                
                
                #if the file name already exist, but the sizes are different

                if file in movie_dict and movie_dict[file][0] != file_size:
                    fhand.write('\n File Name: %s  ||  File1_loc: %s   ||  File2_loc: %s \n\n ------------\n\n'
                                %(file, path, movie_dict[file][1]) )  
                    count2 +=1
                    
                    
                    
                    #If two different movie names have exactly the same size                    
                    
                elif file not in movie_dict and file_size in [i for i,j in movie_dict.values()]:
                    name_of_duplicate = get_file_name(file_size)
                    f2hand.write('\n File1 Name: %s \t Destination1: %s \n\n File2 Name: %s \t Destination2: %s \n ------------\n\n\n\n'
                                 %(file, path, name_of_duplicate, movie_dict[name_of_duplicate][1]))
                    count3 +=1
                    
                    
                    
                    #If the file name already exist and both have the same size
                    #move duplicate file to a predefined destination,based on two criteria: name and size

                elif file in movie_dict and movie_dict[file][0]==file_size :
                    print("\n\n Found a duplicate of : ", file, "\n in : ", path)
                    full_file_name = os.path.join(path,file)
                    

                    #take input on command to execute
                    while True:
                        try:
                            order = input("should i move this file to the 'duplicate_files' folder? yes / No >> \n").lower()
                            if order== 'yes':
                                os.system('move "%s" %s' % ("%s" %full_file_name, duplicate_folder_path))
                                
                                moved_movies.append((file, path))
                                break
                            elif order == 'no':
                                print("duplicate: ", file, "Retained!")
                                break
                            else:
                                print("enter either 'yes' of 'no'!")

                            
                        except:
                            print("enter either 'yes' of 'no'!")
                            
                else:
                    movie_dict[file] = file_size, path
                
                   
            except:
                  
                count4 +=1
                continue
                
                
        count = count+1
        
        
        #print('found:  %s' % os.path.join(path,file))
fhand.close()         
f2hand.close()
print('\n\n\t\t\t\t ---Report---\n\n \n \n' )   
print('\t There was %d  movies in your root directory %s \n \n' % (count, Path_name))                                             
print('\t Found %d Unique movies  \n \n' % len(movie_dict))
print('\t Moved %d Duplicate movies to %s for manual deleting \n \n' % (len(moved_movies), duplicate_folder_path))
print('\t Found %d cases of movies with the same size\n \n' % count3)
print('\t Found %d cases of movies with the same filename \n \n'% count2)
print('\t Found %d Unreadable movies \n \n'% count4)
print("Done!")
