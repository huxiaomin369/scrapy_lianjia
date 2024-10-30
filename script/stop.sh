export BASE_DIR=`../`
pid=`ps ax | grep -i main.py | grep "${BASE_DIR}" | grep python3 | grep -v grep | awk '{print $1}'`
if [ -z "$pid" ] ; then
    echo "No lianjia running."
else
    echo "killed lianjia"
    kill ${pid}
fi

pid=`ps ax | grep -i chrome | grep -v grep | awk '{print $1}'`
if [ -z "$pid" ] ; then
        echo "No lianjia running."
else
    echo "killed chrome"
    kill ${pid}
fi
