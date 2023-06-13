from main import *
from api import *
 
if 'COLAB_GPU' in os.environ:
   threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()
else:
   if __name__ == "__main__":
      app.run()