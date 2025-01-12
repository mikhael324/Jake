if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/mikhael324/Jake.git /Mikhael
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Mikhael
fi
cd /Mikhael
pip3 install -U -r requirements.txt
echo "Starting Mikhael...."
python3 bot.py
