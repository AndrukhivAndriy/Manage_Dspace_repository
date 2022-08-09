# Export/import/backup data from Dspace repository
Those instruments can be usefull for exchanging content between repositories. Script were tested on v6.3 . More info - [https://wiki.lyrasis.org/display/DSDOC6x/AIP+Backup+and+Restore](https://wiki.lyrasis.org/display/DSDOC6x/AIP+Backup+and+Restore).

## Export content - community or collection

*/dspace/bin/dspace packager -u -d -a -t AIP -e admin@email.ua -i 12345678/1111 /home/dump_dspace/open.zip*

	where 12345678/1111 -- handle, community/collection URL 

	/home/dump_dspace/open.zip -- dumped community/collection in zip archive
	
	admin@email.ua -- admin repository email
	
## Import content - community or collection
	
*/dspace/bin/dspace packager -u -r -a -k -t AIP -e admin@email.ua -p 12345678/1111 -o skipIfParentMissing=true /home/dump_dspace/open.zip*

------------------------------------------------------------------------------------------------------------------------------------------
	
When you are trying replace content - will be a problem with community/collection permissions. All permissions will on input user - admin@email.ua . Those scripts can change permissins to disable admin@email.ua and allow to Anonymous read items, bitstream, license, bundle. 
After end of script work you have to run:

	/dspace/bin/dspace cleanup -v
	/dspace/bin/dspace index-discovery -b
      
where *cleanup -v* -- will delete all trash

*index-discovery -b* -- will update search index. After running this command - count of items will be not zero
