import svelte from 'rollup-plugin-svelte';
import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs';
import { terser } from 'rollup-plugin-terser';

export default {
	input: './widget.svelte',
	output: {
		format: 'iife',
		name: 'GoodBot', // Name of the class
		file: 'dist/mywidget.js' // path to the saved widget
	},
	plugins: [
		svelte({
			emitCss: false  // No separate `.css` files.
		}),
		resolve({
			browser: true,
			dedupe: importee => importee === 'svelte' || importee.startsWith('svelte/')
		}),
		commonjs(),
		terser()
	]
};