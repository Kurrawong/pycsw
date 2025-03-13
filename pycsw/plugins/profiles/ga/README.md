# GA Profile

To implement this profile in an instance of pyCSW:

### 1. copy contents

The folder `ga/` that this README file is in, and its contents, heed to be added to the pyCSW installation within the `profiles/` folder:

`pycsw/plugins/profiles/ga`

### 2. register the profile

The profile must be registered in the config file, usually called `default.yml` like this:

```yaml
profiles:
    - apiso
```

becomes

```yaml
profiles:
    - apiso
    - ga
```

A complete example `default.yml` is stored in this profile folder.

### 3. request the profile by `outputSchema`

`GetRecordByID` and similar requests can ask for this profile to be used by quoting `outputSchema=http://pid.geoscience.gov.au/dataset/ga/122551`, e.g.:

`http://localhost:8000/csw?service=CSW&version=2.0.2&request=GetRecordById&Id=GSSA2018D037833&ElementSetName=full&outputSchema=http://pid.geoscience.gov.au/dataset/ga/122551`


## Contact

Contact the author for any needed help:

**Nicholas Car**  
_KurrawongAI_  
<nick@kurrawong.ai>  
<https://kurrawong.ai>  