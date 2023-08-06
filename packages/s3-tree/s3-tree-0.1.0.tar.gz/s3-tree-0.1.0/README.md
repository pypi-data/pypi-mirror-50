# s3-tree  
  
uses the tree command to display the objects in an s3 bucket in a tree-like diagram.  
  
### dependencies  
  
tree  
python3  
aws cli  
  
### installation  
  
`$ pip install s3-tree`  
  
### usage  
  
`$ s3-tree bucketname`  
  
### example  
  
```
$ s3-tree bucketname
bucketname
├── asset-manifest.json
├── favicon.ico
├── index.html
├── manifest.json
├── precache-manifest.e8c8442b93de34204de5f9b23fa0174b.js
├── service-worker.js
└── static
    ├── css
    │   ├── main.43b5e879.chunk.css
    │   └── main.43b5e879.chunk.css.map
    ├── js
    │   ├── 1.f6579156.chunk.js
    │   ├── 1.f6579156.chunk.js.map
    │   ├── main.36bbb0f4.chunk.js
    │   ├── main.36bbb0f4.chunk.js.map
    │   ├── runtime~main.229c360f.js
    │   └── runtime~main.229c360f.js.map
    └── media
        ├── her.37588412.png
        ├── me.e69004b8.png
        └── us.f114bc8d.jpg

4 directories, 17 files
```
