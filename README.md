Steps to create OSM VNFD and NS template from Helm Based Deployment
---------------------------------------------------------------------

1. For each VNFD component, go through the HELM Chart details (Particularly the Values.yaml file and Template directory),
   to understand the KNF Deployment architecture.
   Note down the configurable items from the values.yaml file as these will be used in creating the params.yaml file 
   during Network Service creation.
   
   A typical Helm Chart would have the below mentioned directory structure:
  
```
    +--- helm-pkg-dir
    |   +--- Chart.yaml
    |   +--- templates
    |   |   +--- config.yaml
    |   |   +--- controller.yaml
    |   |   +--- NOTES.txt
    |   |   +--- rbac.yaml
    |   |   +--- service-accounts.yaml
    |   |   +--- speaker.yaml
    |   +--- values.yaml
```  
 
2.  Create a OSM style VNFD directory structure as shown below:
 ```   
    +--- component1_knf
    |   +--- component1_vnfd.yml
    |   +--- helm-chart-v3s
    |   |   +--- componenet1-helm-chart.tgz
 ```

3. Write the VNFD descriptor defination in the `component1_vnfd.yaml` file. 
   The basic VNFD template should contain meta-data inforamtion about the VNFD , one or more KDU Details 
   and External Connection Points. 
   
   Sample VNF Descriptor is shown below.
```
 -----------------------------------------------------------------------------------------------------------------
|vnfd:                                                                                                           |
|  description: 'KNF for deployment of compoenent-1'      # Brief Description about the compoenent               |
|  mgmt-cp: mgmt-ext                                      # Management Connection Point name                     |               
|  product-name: compoenent1_knf                          # Product Meta data.                                   |  
|  provider: Telefonica                                                                                          |
|  version: '1.0'                                                                                                | 
|  df:                                                    # deployment flavour (df) details                      |
|  - id: default-df                                                                                              |
|  ext-cpd:                                               # External Connection Points (ext-cpd)                 | 
|  - id: mgmt-ext                                                                                                |  
|    k8s-cluster-net: mgmtnet                             # k8 cluster network name already provisioned in OSM.  |
|  id: component1_knf                                     # Unique name given for VNFD                           |
|  k8s-cluster:                                           # k8 cluster details                                   |
|    nets:                                                                                                       |
|    - id: mgmtnet                                                                                               |
|  kdu:                                                   # One or more KDU details along with Helm chart name   |
|  - name: componenet1_kdu1                                                                                      |
|    helm-chart: compoenent1-kdu1.tgz                                                                            |
|  - name: compoenent1_kdu2                                                                                      |  
|    helm-chart:  component1-kdu2.tgz                                                                            |
-----------------------------------------------------------------------------------------------------------------
```
4. Create OSM style NS directory sturcture as show below:
 ```
+--- componenet1_ns
|   +--- checksums.txt
|   +--- componenet1_nsd.yaml    # Network Service Descriptor defination
|   +--- params
|   |   +--- params.yaml         # File containing Day-0 Configuratble elements
|   +--- README.md

 ```
5. Write the Network Service Descriptor in the `component1_nsd.yaml` file. 
   The NSD defination should contain NSD Metadata, Constituents VNFs and Virtual link connectivity details.
```
|-----------------------------------------------------------------------------------------------------------------------
|nsd:                                                                                                                   |
|  nsd:                                                                                                                 |
|  - description: NS consisting of a single KNF compoenent-1 connected to management network                            | 
|    designer: OSM                                                                                                      |   
|    df:                                 # Deployment Flavour (df)                                                      |
|    - id: default-df                                                                                                   |
|      vnf-profile:                      # Details regarding Virtual connectivity Link between various constituent KDU  |
|      - id: component1_knf                                                                                             |
|        virtual-link-connectivity:                                                                                     |
|        - constituent-cpd-id:                                                                                          |
|          - constituent-base-element-id: component-1                                                                   |
|            constituent-cpd-id: mgmt-ext                                                                               |
|          virtual-link-profile-id: mgmtnet                                                                             |
|        vnfd-id: compoenent1_knf                                                                                       |
|    id: compoenent1_ns                       # Unique Network Service ID                                               |
|    name: compoenent1_ns                                                                                               |
|    version: '1.0'                                                                                                     |
|    virtual-link-desc:                       # Details regarding external virtual link connectivity                    |
|    - id: mgmtnet                                                                                                      |
|      mgmt-network: 'true'                                                                                             |
|    vnfd-id:                                                                                                           |
|    - component1_knf                        # details of one or more constituent VNFs                                  |
|------------------------------------------------------------------------------------------------------------------------
```

6. Define the `params.yaml` file in the NSD template directory. This file contaions the Day-0 configurable elements. 
   The list of elements is obtained from the Helm-Chart's `values.yaml` file. 
   The `params.yaml` file contains configurable elements for each KDU defined in the VNFD.
   Below is the template for the `params.yaml` file:
   
```
k8s-namespace: application-1
additionalParamsForVnf:
- member-vnf-index: application-component1
  additionalParamsForKdu:
  - kdu_name: compoenent1-kdu1
    additionalParams:
    clusterName: application-cluster
    image: compoenent1-kdu-container-image.23.0-40.tar
    global:
    existingConfigMap:
    images:
      comp1-kdu1:
        name: compoenent1-kdu1
        tag: 1.23.0-40
        resources:
          requests:
            cpu: "50m"
            memory: "250Mi"
          limits:
            cpu: "100m"
            memory: "300Mi"
    updateStrategy:
      # Configuration specific to the speaker DaemonSet
      # type can be OnDelete or RollingUpdate
      type: RollingUpdate
      rollingUpdate:
        maxUnavailable: 25%
  - kdu_name: component2-kdu2
    additionalParams:
    clusterName: applcation-cluster
    image: component2-kdu2.23.0-40.tar
    global:
    existingConfigMap:
    images:
      controller:
        name: compoenent2-kdu2
        tag: 1.23.0-40
        resources:
          requests:
            cpu: "50m"
            memory: "250Mi"
          limits:
            cpu: "100m"
            memory: "300Mi"
        tolerations: []
        affinity: {}
    updateStrategy:
      # Configuration specific to the controller Deployment
      # type can be RollingUpdate or Recreate
      type: RollingUpdate
      rollingUpdate:
        maxUnavailable: 25%
        maxSurge: 25%|  
```
7. Create an archive (tar.gz) of the VNFD directory structure and NSD directory structure and deploy VNFD and NSD using below mentioned commands.

   Command to deploy VNFD package in the OSM 
```
  -->  osm vnfpkg-create component1_vnfd.tar.gz
```
   Command to deploy NS package in the OSM
```
   -->  osm nspkg-create component1_ns.tar.gz
```
   Command to create network service instance
```
   --> osm ns-create compoenent1-ns --vim-account vim-openstack1 --config-file component1-cloud-init-file
```





