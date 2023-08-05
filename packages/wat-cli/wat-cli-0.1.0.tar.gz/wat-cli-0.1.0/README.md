# wat is this?

It's a simple command line tool to get short answers from Wolfram Alpha.

```
> wat is the circumference of the moon`
about 10921 kilometers
```

# wat do i need to do to run this?

You need to get an AppId from Wolfram Alpha. Please visit the
[API Documentation](https://products.wolframalpha.com/api/) website
for further information.

The AppID can be supplied via the `--appid` CLI option or via the configuration
file (`appid="XXXXXX-YYYYYYYYYY"`).

Run `wat --help` to find the location of the configuration file.

# wat even is a kilometer? I want miles!

Use CLI option `--units=imperial` or add `units=imperial` to the configuration
file.

# wat does wat stand for?

Obviously it stands for Wolfram Alpha uhh... Thing.
