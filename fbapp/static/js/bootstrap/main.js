function calc(v){var don=+document.getElementById('don').value;
              var red=(don*0.66).toFixed(2).replace(/(\d)(?=(\d\d\d\b)+)/g,'$1 ');
              var val=(don*0.34).toFixed(2).replace(/(\d)(?=(\d\d\d\b)+)/g,'$1 ');
              var ref='<a href="http://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000018619914&cidTexte=LEGITEXT000006069577" target="_blank">Référence : Code général des impôts - Article 200</a>';
              document.getElementById('rsp').innerHTML='Votre réduction d\'impôts : <span class="red">'+red+' €</span><br>Coût effectif : <b>'+val+'</b> €<br>'+ref;
              document.getElementById('don').value=(+don).toFixed(2).replace(/(\d)(?=(\d\d\d\b)+)/g,'$1 ')+' €';
}