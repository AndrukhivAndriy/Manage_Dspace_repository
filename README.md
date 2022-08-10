# Export/import/backup data from Dspace repository
Those instruments can be useful for exchanging content between repositories. Scripts were tested on v6.3 . More info - [https://wiki.lyrasis.org/display/DSDOC6x/AIP+Backup+and+Restore](https://wiki.lyrasis.org/display/DSDOC6x/AIP+Backup+and+Restore).

## Export content - community or collection via AIP

*/dspace/bin/dspace packager -u -d -a -t AIP -e admin@email.ua -i 12345678/1111 /home/dump_dspace/open.zip*

	where 12345678/1111 -- handle, community/collection URL 

	/home/dump_dspace/open.zip -- dumped community/collection in zip archive
	
	admin@email.ua -- admin repository email
	
## Import content - community or collection via AIP
	
*/dspace/bin/dspace packager -u -r -a -k -t AIP -e admin@email.ua -p 12345678/1111 -o skipIfParentMissing=true /home/dump_dspace/open.zip*

------------------------------------------------------------------------------------------------------------------------------------------
	
When you are trying to replace content - will be a problem with community/collection permissions. All permissions will be on input user - admin@email.ua (only admin can read items). Those scripts can change permissions to disable admin@email.ua and allow to Anonymous read items, bitstream, license, bundle. 
After end of script work you have to run:

	/dspace/bin/dspace cleanup -v
	/dspace/bin/dspace index-discovery -b
      
where *cleanup -v* -- will delete all trash

*index-discovery -b* -- will update search index. After running this command - the count of items will not be zero

## How to work with scripts

1. You have to install/update Python. It works with v3 
2. Intall packet maneger - pip. For Ubuntu -- *sudo apt install python3-pip*
3. install dependencies - *pip install psycopg2-binary*
4. Edit file *change_per_com.py*. Find row 63 *connection = psycopg2.connect* and change all parameters in accordance to your Postgresql server connection. 
5. Edit file *change_per_com.py*. Find row 18 *where email=admin@admin.ua* and change email according to admin email of destination repository 
6. Run script *python3 change_per_com.py*
7. Enter community hande id

--------------------------------------------------------------------------------------------------------------------------------------

### If you can't run the script on database server. 

You have to change */etc/postgresql/9.6/main/pg_hba.conf* by changing the last row according to: 

host	all	dspace	all	trust

and then you can run it from your computer. This row changes access permissions to Dspace database. 

---------------------------------------------------------------------------------------------------------------------------------------

## Import/export collections (for community or sub-community - not working). Info from - [https://wiki.lyrasis.org/display/DSDOC7x/Importing+and+Exporting+Items+via+Simple+Archive+Format](https://wiki.lyrasis.org/display/DSDOC7x/Importing+and+Exporting+Items+via+Simple+Archive+Format)

Export:

	[dspace]/bin/dspace export -t ITEM -i itemID_or_handle -d /path/to/destination -n seq_num

Import:

	[dspace]/bin/dspace import -a -e joe@user.com -c CollectionID -s items_dir -m mapfile
