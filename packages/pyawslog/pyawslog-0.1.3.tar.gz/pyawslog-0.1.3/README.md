# python aws custom log
A Python package to log message into aws cloud.

## Introduction
A Python package to log message into aws cloud.

## Installation
pip3 install pyawslog
## Usage
```
logger = log(region_name='region name', 
          aws_access_key_id='access key',
       aws_secret_access_key='secret key',
        endpoint_url='https://logs.<region_str>.amazonaws.com')

LOG_GROUP='custom group name'
LOG_STREAM='custom stream name'

logger.create_log_group(LOG_GROUP)
logger.create_log_stream(LOG_GROUP, 'aws')
logger.log_message(LOG_GROUP, LOG_STREAM, 'Hello world, log message!')
```
## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
## History
TODO: Write history
## Credits
TODO: Write credits
## License
TODO: Write license
]]></content>
  <tabTrigger>readme</tabTrigger>
</snippet>
## Contact
Please submit an issue if you encounter a bug and please email any questions or requests to catchmaurya@gmail.com