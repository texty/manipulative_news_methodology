const express = require('express')
const app = express()

var bodyParser = require('body-parser');

var readability = require('readability');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

app.use(bodyParser.json({ limit:'100MB', type:'application/json'}));
app.use(bodyParser.urlencoded({ limit:'100MB', extended: true }));

app.post('/', function( req, res ) {
    var doc = new JSDOM( req.body.raw_html );

    var article = new readability(doc.window.document).parse();
    if ( article == null ) {
            var resp = {
            title: '',
            content: ''
        };
        console.log( "Can't process it :((" );
    } else {
            var resp = {
            title: article.title,
            content: article.content
        };
        console.log( article.title );
    }

    res.send( JSON.stringify(resp) );
})

app.listen(3000, () => console.log('Readability node server is ready! Default port - 3000'))