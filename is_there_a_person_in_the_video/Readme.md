# IS THERE A PERSON IN THE VIDEO?
[]: # Author: [Raúl Sánchez](raul@um.es)
[]: # Date: 2022-10-10
[]: # License: MIT
[]: # Tags: video, person, detection, object, detection, opencv, python
[]: # Description: This is a simple script to detect if there is a person in a video. It uses openpose (nose and shoulders) to check it.

# Description

Little script to detect if there is a person in a video. It uses openpose (nose and shoulders).

I have created a Docker image where is openpose installed. You can find it in [Docker Hub](https://hub.docker.com/r/raulkite/is_there_a_person_in_the_video).

This way you can also use openpose with python bindings without installing it in your computer (requires GPU).

# Usage

```bash
docker run -it --gpus all  -v $PWD/videos:/videos -v $PWD/YES:/YES -v $PWD/NO:/NO is_there_a_person_in_the_video:0.1 python3 /openpose/is_there_a_person_in_the_video.py --videos /videos --discarded_videos /NO --matched_videos /YES
```

