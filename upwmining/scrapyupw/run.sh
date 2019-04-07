#  Run Scrapy from Docker 
#  docker exec -i -t sparkc sh work/upwmining/scrapyupw/run.sh

cd work/upwmining/scrapyupw

echo "*****  Running Upw Spider on $PWD  *****" 

dataFile=upwdata__$(date "+%Y%m%d_%H%M%S").jl
logFile=upwmining__$(date "+%Y%m%d_%H%M%S").log 

#scrapy crawl upw --s CLOSESPIDER_PAGECOUNT=500 -o $dataFile -s LOG_FILE=$logFile
scrapy crawl upw --s CLOSESPIDER_PAGECOUNT=5 -o $dataFile #-s LOG_FILE=$logFile