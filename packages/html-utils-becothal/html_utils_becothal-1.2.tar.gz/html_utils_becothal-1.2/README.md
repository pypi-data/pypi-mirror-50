# HTML utils 
## Removing Comments from files 
Comments are not being removed when: 
 - there is a `"` or a `'` in the same line.
 - there is a `[finalComment]` in the Comment.
 All other Comments are removed.
 ### Usage 
 `file_model.removeComments(<SinglelineComments>,<MultilineCommentStart>,<MultilineCommentEnd>)`\
 `jsFile.removeComments("//", "/*", "*/")`
 
 ## Uglify
 Uglify removes all the `\n` 
 ### Usage
 `file_model.uglify()`
 
 ## Change images to base64
 Replaces the source in `<img>`-Tags with the Base64 String of the image.
 Accepted image types are:
  - bmp
  - gif
  - jpeg
  - png
  - svg
 ### Usage 
 `file_model.imagesToBase64()`