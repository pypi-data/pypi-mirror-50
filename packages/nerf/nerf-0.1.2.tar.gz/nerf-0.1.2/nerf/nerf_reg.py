#%%
# calculating the I(Fi, Fj) while generating the edge intensity
# Take the output of nerftab() to generate the network ready table for the NERF progress
# Yue Zhang <yue.zhang@lih.lu>
# Oct 2018



def timing(func):
    def wrap(*args, **kw):
        print('<function name: {0}>'.format(func.__name__))
        time1 = time.time()
        ret = func(*args, **kw)
        time2 = time.time()
        print('[timecosts: {0} s]'.format(time2-time1))
        return ret
    return wrap


@timing
def localnerf(nf_ff, local_index):
    try:
        allpairs_local = nf_ff[1].loc[(nf_ff[1]['sample_index'] == local_index, )]
        allpairs_local['GSP'] = (allpairs_local.loc[:, 'GS_i'] + allpairs_local.loc[:, 'GS_j'])
        localtable = allpairs_local.groupby(['feature_i', 'feature_j'], as_index = False)['GSP'].agg([np.size, np.sum]).reset_index()
        localtable['EI'] = localtable.values[:, 3] * localtable.values[:, 2]
        output_local = localtable.loc[:, ['feature_i','feature_j','EI']]

        return output_local
    except TypeError as argument:
        print("Process disrupted, non-valid input type ", argument)

# This is like 1000+ times faster...
# Try to be smart otherwise you are screwed up


# Sort by value, Dict
def sort_by_value(d):
    items = d.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort(reverse=True)
    return [backitems[i][1] for i in range(0, len(backitems))]


# Define a func for later
@timing
def twonets(outdf, filename, index_of_features, featureref, index1=4, index2=11):
    """
    Purpose
    ---------
    Process the result of the localnerf(), return two networks, one with everything, one with less info
    ---------
    :param outdf: The localnerf() result
    :param filename: the desire filename, or path with name, no suffix
    :param index1: Index for selecting top degree of centrality, default = 2
    :param index_of_features: The original order of all the features, set to false as D
    :param featureref: The target feature reference, e.g., gene symbols, set to false as D
    :param index2: Index for selecting top edge intensity, default = 10
    :return: A list contains five elements, whole network with gene names, degree of all features,
     degreetop selected, eitop delected, sub network with gene names
    """
    if not os.path.exists("output"):
        os.makedirs("output")
    if index_of_features or featureref:
        outdf = outdf.replace(index_of_features, featureref)

    else:
        pass
    # export the 'everything' network
    outdf.to_csv(os.getcwd() + '/output/' + filename + "_everything.txt", sep='\t')

    gout = nx.from_pandas_edgelist(outdf, "feature_i", "feature_j", "EI")

    degreecout = nx.degree_centrality(gout)
    # Test save the centrality
    degreecoutdf = pd.DataFrame.from_dict(degreecout, orient="index")
    degreecoutdf.to_csv(os.getcwd() + '/output/' + filename + "_DC.txt", sep='\t')
    # Large to small sorting
    sortdegree = sort_by_value(degreecout)
    # take the top sub of the DC
    degreetop = sortdegree[: int(index1 * math.sqrt(len(sortdegree)))]
    # Large to small sorting, Edge intensity
    outdfsort = outdf.sort_values('EI', ascending=False)

    eitop = outdfsort[: int(index2 * math.sqrt(outdfsort.shape[0]))]

    outdffinal = eitop[eitop['feature_i'].isin(degreetop) & eitop['feature_j'].isin(degreetop)]
    outdffinal.to_csv(os.getcwd() + '/output/' + filename + '_sub.txt', sep='\t')
    outputfunc = list()
    outputfunc.extend((outdf, degreecout, degreetop, eitop, outdffinal))
    print("Processing finished.")
    return outputfunc



