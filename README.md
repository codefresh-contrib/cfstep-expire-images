# cfstep-expire-images
Tool for expiring Docker images by removing their tags after passing expiration date

To keep your Codefresh Registry clean we can add metadata to your Docker images to expire them on a specific date.

Using an ad-hoc pipeline and setting up a CRON schedule we'll be able to run this pipeline step and determine which Docker images are past their expiration date and remove tags from those images so they no longer show in your Docker image Artifacts listing.

Add these 2 metadata annotations to any step where you'd like to set an expiration date on your images.

EXPIRATION - true
DTE - Days Until Expiraton

``` yaml
steps:
  build_step:
    type: build
    ...
    metadata: # Declare the metadata attribute
      set: # Specify the set operation
        - EXPIRATION: true
        - DTE: 14
```

Setup an ad-hoc pipeline and CRON using the YAML below to schedule the deletion.

``` yaml
version: '1.0'
steps:
  ExpireImages:
    image: codefresh/cfstep-expire-images:latest
```

If you find yourself in a pinch and need to add to DTE or remove the expiration on an image please see commands below.

`codefresh annotate image 6a85261f041e --label DTE=365`
`codefresh annotate image 6a85261f041e --label EXPIRATION=false`