import pickle
import numpy as np 


def calculate_transition_probabilities(links , attributes , w = [1.,1.]):

    n,temp  = links.shape   
    num_attr = 1
    print (n+num_attr*2, n+num_attr*2)
    transition_p = np.zeros( (n+num_attr*2, n+num_attr*2) , dtype='float')

    w = np.ones(1+2*num_attr , dtype='float')
    
    for i in range(n):
        
        # Calculating transitions from vertices to vertices.
        total_neighbours = np.sum(links[i])
        transition_p[i][np.where(links[i]==1)] = w[0]/(total_neighbours*w[0] + w[1])
        
        # calculating transitions from vertices to attribute vertices.
        if attributes[i] == 0:
            transition_p[i][n] = w[1]/(total_neighbours*w[0] + w[1])
        else:
            transition_p[i][n+1] = w[1]/(total_neighbours*w[0] + w[1])

    # Calculating transitions from attribute vertices to vertices.
    attribute_neighbours = np.zeros(2)
    attribute_neighbours[0] = np.where(attributes==0)[0].size
    attribute_neighbours[1] = np.where(attributes==1)[0].size

    transition_p[n][np.where(attributes==0)] = 1./attribute_neighbours[0]
    transition_p[n+1][np.where(attributes==1)] = 1./attribute_neighbours[1]

    return transition_p


def calculate_random_walk_distance(transition_p , n , c=0.2 , l=2):

    n , temp = transition_p.shape
    n -= 2
    
    # Calculating the random walk distance between any two points with maximum l jumps
    random_d = np.zeros(transition_p.shape ) 
    for gamma in range(1,l+1):
        random_d += c*(1-c)*np.linalg.matrix_power(transition_p , gamma)

    random_d = random_d[:n,:n]
    return random_d


def cluster(random_d , n , k=7, sigma=1):

    # Calculating node densities.
    # densities = np.ones(random_d.shape) - np.exp(-np.square(random_d)/(sigma**2))
    densities = 1 - np.exp(-np.square(random_d)/(sigma**2))
    densities = np.sum(densities,axis=0)
    # Selecting K initial centroids. 
    centroids = np.argsort(densities)[-k:][::-1]

    # K mediod Clustering 
    convergence = False
    assignments = np.zeros(n , dtype='int')
    old_assignments = np.copy(assignments)
    cluster_averages = np.empty((k,n))
    
    iteration=0
    while not convergence and iteration < 20:

        # print assignments.shape
        # assign nodes to nearest clusters.
        for i in range(n):
            assignments[i] = np.argmax(random_d[i,centroids])
            # print "Cluster for node" , i , assignments[i]


        # print assignments.shape
        # Check for convergence.
        if np.array_equal(assignments , old_assignments):
            convergence = True

        old_assignments = np.copy(assignments)

        # Find distance of cluster from graph and assign new centroid
        for i in range(k):
            current_members = np.where(assignments==i)[0]
            
            cluster_averages[i] = np.mean(random_d[current_members, :],axis=0)
            
            # Assign new centroid
            
            if current_members.size != 0:
                node_cluster_distances = np.zeros(current_members.size)
                # print current_members , current_members.size

                for j,node in enumerate(current_members):
                    node_cluster_distances[j] = np.linalg.norm(random_d[node] - cluster_averages[i])

                centroids[i] = current_members[np.argmin(node_cluster_distances)]


        # Printing cluster members
        print "Iteration:",iteration 

        for i in range(k):
            current_members = np.where(assignments==i)[0]
            print "Cluster" , i , "Members" , current_members.size            
        # Calculating the objective function.
        obj = 0.
        for i in range(k):
            current_members = np.where(assignments==i)[0]
            if current_members.size != 0:
                obj += np.mean(random_d[current_members , current_members])

        print obj

        iteration+=1

        

attribute_links = pickle.load(open('pol_data.p','rb'))
links = attribute_links['links']
attributes = attribute_links['attributes']

n , temp = links.shape

c = 0.2
l = 2


transition_p = calculate_transition_probabilities(links,attributes)
random_d = calculate_random_walk_distance(transition_p,n)
cluster(random_d , n)


