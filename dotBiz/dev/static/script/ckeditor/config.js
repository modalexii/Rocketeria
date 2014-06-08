/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here.
	// For complete reference see:
	// http://docs.ckeditor.com/#!/api/CKEDITOR.config
	 CKEDITOR.stylesSet.add( 'my_styles', [
		// Block-level styles
		{ 
			name: 'Normal', 
			element: 'p', 
			styles: { '*':'inherit !important' }
		},
		{ 
			name: 'Testimonial',
			element: 'p',
			styles: { 'border-bottom':'1px solid #0f0403', 'padding-bottom':'12px', 'padding-top':'12px' },
			attributes: { 'class': 'testimonial' }
		},
		// Inline styles
		{ name: 'Big', element: 'big', },
		{ name: 'Quote Feed',
			element: 'span', 
			attributes: { 'class': 'quote_feed' }
		},
		{ name: 'Highlight: R', element: 'span', styles: { 'background-color': '#f97b7d' } },
		{ name: 'Highlight: G', element: 'span', styles: { 'background-color': '#9df860' } },
		{ name: 'Highlight: B', element: 'span', styles: { 'background-color': '#abfffc' } },
		{ name: 'Highlight: Y', element: 'span', styles: { 'background-color': '#f5ed14' } },
		{ name: 'Highlight: P', element: 'span', styles: { 'background-color': '#e26ffb' } },
	] );

	config.stylesSet = 'my_styles';

	// The toolbar groups arrangement, optimized for two toolbar rows.
	config.toolbarGroups = [
		{ name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
		{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
		{ name: 'links' },
		{ name: 'insert' },
		{ name: 'forms' },
		{ name: 'tools' },
		{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
		{ name: 'others' },
		'/',
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
		{ name: 'styles' },
		{ name: 'colors' },
		{ name: 'about' }
	];

	// Remove some buttons provided by the standard plugins, which are
	// not needed in the Standard(s) toolbar.
	config.removeButtons = 'Underline,Subscript,Superscript';

	// Set the most common block elements.
	config.format_tags = 'p;h1;h2;h3;pre';

	// Simplify the dialog windows.
	config.removeDialogTabs = 'image:advanced;link:advanced';
};
