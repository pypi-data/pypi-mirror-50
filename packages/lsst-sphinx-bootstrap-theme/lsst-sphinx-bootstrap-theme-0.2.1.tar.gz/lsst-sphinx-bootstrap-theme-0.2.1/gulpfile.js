const autoprefixer = require('autoprefixer');
const cleanCss = require('gulp-clean-css');
const gulp = require('gulp');
const minimist = require('minimist');
const run = require('gulp-run');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');
const postcss = require('gulp-postcss');
const noop = require('gulp-noop');

// parse command line options
// [--env dev (default) | prod]
const options = minimist(process.argv);
const env = options.env || 'dev';

// Environment-based configurations for CleanCss
// https://github.com/jakubpawlowicz/clean-css
const cleanCssConfig = {
  dev: {
    compatibility: '*',
    level: 2,
    format: 'beautify'
  },

  prod: {
    compatibility: '*',
    level: 2
  }
};

/*
 * gulp environment
 * Prints the environment setting.
 */
function environment() {
  console.log(`${env}`);
  return Promise.resolve();
}

exports.environment = environment;

/*
 * gulp scss
 * Compile the sass
 */
function scss() {
  return (
    gulp
      .src('scss/app.scss')
      // Initialize sourcemaps
      .pipe(sourcemaps.init())
      .pipe(env === 'dev' ? sourcemaps.init() : noop())
      // Compile sass synchronously
      .pipe(sass.sync().on('error', sass.logError))
      // Autoprefix with default configs
      .pipe(postcss([autoprefixer()]))
      // Clean CSS
      .pipe(env === 'dev' ? sourcemaps.write() : noop())
      .pipe(cleanCss(cleanCssConfig[env]))
      .pipe(gulp.dest('lsst_sphinx_bootstrap_theme/static'))
  );
}

exports.scss = scss;

/*
 * gulp watch
 * Watch for source changes and rebuild any assets
 */
function watch() {
  gulp.watch(['scss/*.scss'], {}, gulp.series('sass'));
}

exports.watch = watch;

/*
 * gulp pretty
 * Run Prettier to autoformat code.
 */
function pretty() {
  return run('npm run pretty').exec();
}

exports.pretty = pretty;

/*
 * gulp
 * Default task that compiles assets and watches for additional changes.
 */
exports.default = gulp.parallel(scss, watch);
