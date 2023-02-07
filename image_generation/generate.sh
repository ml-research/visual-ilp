blender --background --python render_vilp.py -- --dataset member --num_images 100 --use-gpu 1 &
blender --background --python render_vilp.py -- --dataset delete --num_images 100 --use-gpu 1 &
blender --background --python render_vilp.py -- --dataset append --num_images 100 --use-gpu 1 &
blender --background --python render_vilp.py -- --dataset reverse --num_images 100 --use-gpu 1 &
blender --background --python render_vilp.py -- --dataset sort --num_images 100 --use-gpu 1 &