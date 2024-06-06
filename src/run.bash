source ./catkin_ws/devel/setup.bash
bash ./bash_scripts/start_control_pc.sh -i localhost

export QUART_APP=src/app
export QUART_ENV=development

export OPENAI_API_KEY="API-key"
quart run
