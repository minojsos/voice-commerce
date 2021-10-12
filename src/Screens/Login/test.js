import AudioRecord from 'react-native-audio-record';

useEffect(() => {
  const options = {
    sampleRate: 16000, // default 44100
    channels: 1, // 1 or 2, default 1
    bitsPerSample: 16, // 8 or 16, default 16
    audioSource: 6, // android only (see below)
    wavFile: 'test.wav', // default 'audio.wav'
  };

  AudioRecord.init(options);

  console.log('use effect home');
}, []);
onPress = {record};

const record = () => {
  console.log('record');

  AudioRecord.start();
  timeout;
  let timeout = setTimeout(() => {
    stopRecord();
    console.log('hello');
  }, 5000);
};

const stopRecord = async () => {
  console.log('recordStop ');
  const audioFile = await AudioRecord.stop();
  AudioRecord.on('data', (data) => {});
  console.log('audioFile 🍷', audioFile);
  initialRec(audioFile);
  // AudioRecord.stop();
};
const initialRec = (audioFile) => {
  uploadAudio(audioFile);
  console.log('initialRec', audioFile);
  const options = {
    sampleRate: 16000, // default 44100
    channels: 1, // 1 or 2, default 1
    bitsPerSample: 16, // 8 or 16, default 16
    audioSource: 6, // android only (see below)
    wavFile: 'test.wav', // default 'audio.wav'
  };
};
const uploadAudio = async (fileUrl) => {
  console.log('upload');
  console.log('🧑‍🚀🧑‍🚀', fileUrl);
  let formData = new FormData();
  formData.append('audioFile', {
    uri: 'file:///data/user/0/com.easy_boiler/files/test.wav',
    type: 'audio/wav',
    name: 'test.wav',
  });
  formData.append('flag', 'name');
  console.log(formData);

  fetch('http://b0a48274d10c.ngrok.io/navigation/en', {
    method: 'POST',
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((response) => {
      console.log('response 🔥', response.flag);
      console.log(response);
      if (!response.flag === 'navigation-error') {
        navigation.navigate(response.flag);
      } else {
        console.log('route error');
      }
    })
    .catch((err) => console.error(err));
};
