# Pseudo Code for 218 work

1. remap status messages to numeric values (purge -> 0, etc.)
2. Create column for differences to flag status changes
   1. Dataframe for text column changes: df_change = df[df["TEXT_COLUMN"].shift() != df["TEXT_COLUMN"]]
3. Flag specific times as "purge complete"
4. Mark regions starting from complete flag and going for 2 minutes or next status change or [define conditions here] as an active test point
   1. Probably need a separate list of these status change timestamps to "find next status change"
   2. Autonumber these regions sequentially, maybe also try to join in test point identifiers from test point matrix based on "closest to start time value"
5. Create new dataframe where test point number is index and each test point is summarized with information similar to the following. This will probably require applying the test point number math to other record codes to ba able to merge them into the master test point data frame
   1. start time
   2. end time
   3. number of targets seen
   4. max accuracy (min uncertainty region volume)
      1. calculate area of ellipse (pi*major*minor)
   5. range
   6. 