# %% __main__
if __name__ == "__main__":
    from mitfat import flags
    from mitfat.file_io import read_data
    import os
    # %% flags
    if_save_eps = False  # if save plots in .eps format. All are saved in .png format by default.
                        # if setting it to True casues some warning messages, just ignore them.

    if_plot_basics = False  # plot normalised time-series, or raw if you do not normalise the data
    if_plot_lin_reg = False  # plots of linearised siganls, separately for each time-degment.
    if_plot_raw = False  #  plot raw time-series

    if_cluster = True  # if cluster and then dave plots for [2, ..., 9] clusters.
    if_cluster_hiararchical = True  # if hierarchical cluster and then save.

    if_detrend = True  # if detrend and save

    # %% look at the sample_info_file.txt for info on how to setup the info.file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    info_file_name = 'sample_info_file.txt'
    info_file_name = os.path.join(dir_path, info_file_name)
    print(info_file_name)

    # %% read the data based on the info in info_file_name
    dataset1 = read_data(info_file_name)
    print(dataset1.description)
    # Basic plots
    if if_plot_basics:
       dataset1.plot_basics()

    if if_plot_lin_reg:
       dataset1.plot_basics('lin_reg')

    if if_plot_raw:
       dataset1.plot_basics('raw')

    if if_cluster:
        ###
        X_train = dataset1.data_normalised
        X_train_label = 'RAW_Normalised'
        print('-----------------------------------')
        print('Clustering ', X_train_label)
        for num_clusters in [2, 3, 4, 5,]:
            print(num_clusters, 'clusters')
            cluster_labels, cluster_centroid = \
                dataset1.cluster(X_train, num_clusters)
            dataset1.save_clusters(X_train, X_train_label,
                                    cluster_labels, cluster_centroid)
            dataset1.plot_clusters(X_train, X_train_label,
                                    cluster_labels, cluster_centroid)
        ###
        X_train = dataset1.data_mean
        X_train_label = 'Mean_Normalised'
        print('-----------------------------------')
        print('Clustering ', X_train_label)
        for num_clusters in [3, 4, 5, 6,]:
            print(num_clusters, 'clusters')
            cluster_labels, cluster_centroid = \
                dataset1.cluster(X_train, num_clusters)
            dataset1.save_clusters(X_train, X_train_label,
                                    cluster_labels, cluster_centroid)
            dataset1.plot_clusters(X_train, X_train_label,
                                    cluster_labels, cluster_centroid)
        ###
        X_train = dataset1.line_reg_slopes
        X_train_label = 'Lin_regression_slopes_per_segments'
        print('-----------------------------------')
        print('Clustering ', X_train_label)
        for num_clusters in [5, 6, 7, 8,]:
            print(num_clusters, 'clusters')
            cluster_labels, cluster_centroid = \
                dataset1.cluster(X_train, num_clusters)
            dataset1.save_clusters(X_train, X_train_label,
                                    cluster_labels, cluster_centroid)
            dataset1.plot_clusters(X_train, X_train_label,
                                    cluster_labels,
                                    cluster_centroid, if_slopes=True)
        ###
        X_train = dataset1.mean_segments
        X_train_label = 'Mean_Segments'
        print('-----------------------------------')
        print('Clustering ', X_train_label)
        for num_clusters in [2, 3, 4, 5,]:
            print(num_clusters, 'clusters')
            cluster_labels, cluster_centroid = dataset1.cluster(X_train, num_clusters)
            dataset1.save_clusters(X_train, X_train_label,
                                    cluster_labels, cluster_centroid)
            dataset1.plot_clusters(X_train, X_train_label,
                                    cluster_labels, cluster_centroid)

    if if_cluster_hiararchical:
        signal = 'raw'
        dataset1.cluster_hierarchial(signal, if_save_plot=True)

    if if_detrend:
        dataset1.detrend()
