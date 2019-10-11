if [ -z "$ROBOT" ]
then
  echo "No robot host provided, provide ENV variable ROBOT"
else
  echo "scp ./ant/backend.py $ROBOT:."
fi


