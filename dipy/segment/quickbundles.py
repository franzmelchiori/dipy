import numpy as np
from dipy.tracking.metrics import downsample
from dipy.tracking.distances import local_skeleton_clustering
from dipy.tracking.distances import bundles_distances_mdf


class QuickBundles(object):
    
    def __init__(self,tracks,dist_thr=4.,pts=12):
        """ Highly efficient trajectory clustering 
        
        Parameters
        -----------
        tracks : sequence of (N,3) ... (M,3) arrays,
                    trajectories (or tractography or streamlines)
                    
        dist_thr : float, 
                    distance threshold in the space of the tracks
        pts : int, 
                number of points for simplifying the tracks 
                       
        Methods
        --------
        clustering() returns a dict holding with the clustering result
        virtuals() gives the virtuals (track centroids) of the clusters
        exemplars() gives the exemplars (track medoids) of the clusters        
        
        Citation
        ---------
        
        E.Garyfallidis, "Towards an accurate brain tractography", PhD thesis, 2011 
        
        """
        self.dist_thr = dist_thr
        self.pts = pts
        if pts!=None:                        
            self.tracksd=[downsample(track,self.pts) for track in tracks]
        else:
            self.tracksd=tracks                    
        self.clustering=local_skeleton_clustering(self.tracksd, self.dist_thr)
        self.virts=None
        self.exemps=None                
    
    def virtuals(self):
        if self.virts==None:
            self.virts=[self.clustering[c]['hidden']/np.float(self.clustering[c]['N']) for c in self.clustering]
        return self.virts       
    
    def exemplars(self,tracks=None):
        if self.exemps==None:            
            self.exemps=[]
            self.exempsi=[]
            C=self.clustering
            if tracks==None:
                tracks=self.tracksd            
            for c in C:
                cluster=[tracks[i] for i in C[c]['indices']]                
                D=bundles_distances_mdf([C[c]['hidden']/float(C[c]['N'])],cluster)
                D=D.ravel()
                si=np.argmin(D)
                self.exempsi.append(si)
                self.exemps.append(cluster[si])                               
        return self.exemps, self.exempsi
    
    def partitions(self):
        return self.clustering
    
    def clusters(self):
        return self.clustering
    
    def label2cluster(self,id):
        return self.clustering[id]
    
    def label2tracksids(self,id):
        return [i for i in self.clustering[id]['indices']]        
    
    def label2tracks(self,tracks,id):
        return [tracks[i] for i in self.clustering[id]['indices']]
       
    def total_clusters(self):
        return len(self.clustering)
        
    def downsampled_tracks(self):
        return self.tracksd
    
    def remove_cluster(self,id):
        print('Not implemented yet')
        pass
    
    def remove_clusters(self,list_ids):
        print('Not implemented yet')
        pass
    
    def remove_tracks(self):
        print('Not implemented yet')
        pass
    
    def points_per_track(self):
        print('Not implemented yet')
        pass
        
        
    
class pQuickBundles():
    
    def __init__(self):
        pass
            
