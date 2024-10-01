const express = require('express');
const {ytdown } = require("nayan-media-downloader")
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const app = express();
const ffmpeg = require('fluent-ffmpeg');
const ffmpegInstaller = require('@ffmpeg-installer/ffmpeg');
const { PassThrough } = require('stream');

const { ytmp3 } = require('y2mate-dl');
const youtubedl = require('youtube-dl-exec')
const ytdl = require('ytdl-core');

const { Innertube } =require ('youtubei.js');

process.env.YTDL_NO_UPDATE = '1';


ffmpeg.setFfmpegPath(ffmpegInstaller.path);

app.get('/download',async function (req, res) {
    console.log(1)
    const youtubeUrl = `https://www.youtube.com/watch?v=${req.query.videoUrlId}`;

    const result = await getDownloadLink(youtubeUrl);

    console.log(result)

    return res.send(result)
    // try {
    //   const youtube = await Innertube.create();
    //   const y = await youtube.download(req.query.videoUrlId)
    //   if(y instanceof ReadableStream){
    //     const reader = y.getReader();

    //     const passThrough = new PassThrough();

    //     const { done, value } = await reader.read();

    //     passThrough.write(value);


    //     console.log(passThrough)

    //   }

    //   const videoInfo = await youtube.getInfo(req.query.videoUrlId);
    //   const manifest = await videoInfo.toDash(url => {
    //     return url;
    //   });
     
    
    //   // Lấy URL của stream đầu tiên (bạn có thể thay đổi tuỳ theo nhu cầu)

    //     // let result = await ytdown("https://www.youtube.com/watch?v=rfzsyIzXwgk")
    //     const youtubeUrl = `https://youtu.be/${req.query.videoUrlId}`

    //     const resultYtdown = await ytdown(youtubeUrl)

    //     console.log(resultYtdown)

    //     let stream

    //     if(resultYtdown.status && resultYtdown.data?.video_hd){
    //       console.log('ytdown')

    //       const videoHdUrl = resultYtdown.data.video_hd

    //       stream = await axios({
    //         url: videoHdUrl,
    //         method: 'GET',
    //         responseType: 'stream',
    //         family: 4
    //       });
    //     }else{
    //       console.log('ytdl')
    //       stream = ytdl(youtubeUrl)
    //     }
        

    //     return res.send(stream)

    //     let result = await ytdown(`https://youtu.be/${req.query.videoUrlId}`)
    //     console.log(result)
        
    //     return res.send(result)

    //     const outputPath = path.resolve(__dirname, `${new Date().getTime()}.mp3`);

    //     // const videoHdUrl = result.data.audio
    //     const videoHdUrl = result.data.video_hd

    //     const response = await axios({
    //         url: videoHdUrl,
    //         method: 'GET',
    //         responseType: 'stream',
    //         family: 4
    //       });
      
    //     const writer = fs.createWriteStream(outputPath);

    //     ffmpeg(response.data)
    //     .audioCodec('libmp3lame')  
    //     .format('mp3')             
    //     .pipe(writer); 

    //       // response.data.pipe(writer);

    //       writer.on('finish', () => {
    //         console.log(`Video đã được tải xuống thành công: ${outputPath}`);
    //       });
      
    //       writer.on('error', (err) => {
    //         console.error(`Lỗi khi ghi file: ${err}`);
    //       });
    // } catch (error) {
    //     console.log(error)
    // }
    
  res.send('Hello World!');
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});

async function getDownloadLink(youtubeUrl) {
  console.log(2)
  try {
    const output = await youtubedl(youtubeUrl, {
      dumpSingleJson: true,  
      noWarnings: true,    
      noCallHome: true,      
      preferFreeFormats: true,
      youtubeSkipDashManifest: true, 
    });

    console.log('output', output)

    // Lấy link download có chất lượng cao nhất
    const bestFormat = output.formats.find(format => format.acodec !== 'none' && format.vcodec !== 'none');
    if (bestFormat && bestFormat.url) {
      return bestFormat.url;
    } else {
      throw new Error('Không tìm thấy link download.');
    }

  } catch (error) {
    console.error('Lỗi:', error);
    throw error;
  }
}