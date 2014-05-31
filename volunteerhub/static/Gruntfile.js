module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    sass: {
      options: {
        includePaths: ['bower_components/foundation/scss']
      },
      foundation: {
        options: {
          outputStyle: 'compressed'
        },
        files: {
          'foundation/css/foundation.min.css': 'src/assets/scss/app.scss'
        }
      }
    },

    watch: {
      grunt: {
        files: ['Gruntfile.js'],
        tasks: ['sass']
      },

      sass: {
        files: 'src/assets/scss/**/*.scss',
        tasks: ['sass']
      },
    }
  });

  grunt.loadNpmTasks('grunt-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-newer');

  grunt.registerTask('build', ['sass']);
  grunt.registerTask('default', ['build','watch']);
}
