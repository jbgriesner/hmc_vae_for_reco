# Datasets

- Here are the 4 datasets for the experiments.
- The raw datasets are in the `./raw` folder.
- The clean datasets are (or will be...) in the `./clean` folder (_clean_ means _after processing_).
- The `movielens100k` is a smaller dataset, so its purpose is for quick iteration.
- **NB**: To avoid the github restriction on max file size of 100MB, the data have been splitted into smaller files. For re-assembling the pieces together to have all checkins in one single file, you can use the simple `cat` tool as follows for instance on foursquare:
```shell
cd ./raw/foursquare
cat checkins_* > checkins
```

## Characteristics:

| Dataset         | #users   | #items   | #clicks   | Density   | Source                                                                                           |
| :-------------: | :------: | :------: | :-------: | :-------: | ------------------------------------------------------------------------------------------------ |
| movielens100k   | 0.6 K    | 9 K      | 0.1 M     | 1.85 %    | [movielens100k](https://grouplens.org/datasets/movielens/)                                       |
| gowalla         | 319 K    | 2844 K   | 36 M      | 0.004 %   | [gowalla](http://www.yongliu.org/datasets/)                                                      |
| foursquare      | 266 K    | 3680 K   | 33 M      | 0.003 %   | [foursquare](https://sites.google.com/site/yangdingqi/home/foursquare-dataset)                   |
| movielens25M    | 162 K    | 62 K     | 25 M      | 0.25 %    | [movielens25M](https://grouplens.org/datasets/movielens/)                                        |

## Processing:
- The output of the processing is expected to be a _clean_ dataset (_ie_. ready for the experiments).

- **Binarization**: To get a clean dataset, the processing will first binarize the data. For `movielens` datasets (both of them) it only requires to convert the explicit ratings into a 0 or a 1 as follows: for each pair `(<user>,<item>)` we keep only ratings higher or equal to 4. However for the 2 other datasets (_ie_ `gowalla` and `foursquare`) it first requires to aggregate the checkins (_ie_ the pairs `(<user>,<location>)` into tuples `(<user>,<location>,<frequency>)`) because the pairs exist at different times. Then we can binarize by keeping only tuples with a `frequency` of at least 10.

- **Train**/**Tune**/**Test Split**: Once the datasets have been binarized, we can split each of them into 3 different subsets for training, tuning and testing models. We want that any user (and any item) in the tune and test sets also exists in the training set. To this end, for each user in the data, if the user has more than 10 different selections, then we put 70% of these selections into the training set, 10% into the tune set and the remaining 20% into the test set. Otherwise we just keep the user into the train set **only** if he has at least 4 different selections.
