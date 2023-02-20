export CUDA_VISIBLE_DEVICES=3
nohup /usr/bin/blender-2.78c-linux-glibc219-x86_64/blender --background --python render_vilp.py -- --dataset member --num_images 100 &
nohup /usr/bin/blender-2.78c-linux-glibc219-x86_64/blender --background --python render_vilp.py -- --dataset delete --num_images 100 &
nohup /usr/bin/blender-2.78c-linux-glibc219-x86_64/blender --background --python render_vilp.py -- --dataset append --num_images 100 &
nohup /usr/bin/blender-2.78c-linux-glibc219-x86_64/blender --background --python render_vilp.py -- --dataset reverse --num_images 100 &
nohup /usr/bin/blender-2.78c-linux-glibc219-x86_64/blender --background --python render_vilp.py -- --dataset sort --num_images 100 &