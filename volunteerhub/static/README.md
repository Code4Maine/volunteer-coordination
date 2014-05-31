# Building Styles

Install all the dependincies: `npm install && bower install`

While you're working on your project, run:

`grunt`

This will compile all the Sass. You're set!

If you'd like to build project files whenever a change is detected, run:

`grunt watch`

Grunt will look for saved files in the src directories and build when needed.

## Directory Structure

* `foundation/css`: Foundation CSS files are assembled here. **Do not edit these directly, they will be overridden when changes are compiled**
* `src/assets/scss`: Make style changes here. These files will be compiled into the complete CSS.
