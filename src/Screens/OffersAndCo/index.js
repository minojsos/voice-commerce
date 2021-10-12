/* eslint-disable react-native/no-inline-styles */
import React, {useEffect, useState} from 'react';
import {View, Text} from 'react-native';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
import {Container, HeaderButton} from '../../Components';
import useAppTheme from '../../Themes/Context';
import {IconX, ICON_TYPE} from '../../Icons';
import {useStoreState} from 'easy-peasy';
import Fonts from '../../Themes/Fonts';
import {TouchableOpacity} from 'react-native';
import {ButtonX} from '../../Components';
import metrics from '../../Themes/Metrics';
import AudioRecord from 'react-native-audio-record';
import AsyncStorage from '@react-native-community/async-storage';
import Tts from 'react-native-tts';

const MainScreen = ({routes, route, navigation}) => {
  const [resList, setListData] = useState('');

  const {theme} = useAppTheme();
  // eslint-disable-next-line prettier/prettier
  const {username, password} = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));

  useEffect(() => {
    getData();
    console.log('👾👾', resList);

    const _toggleDrawer = () => {
      navigation.toggleDrawer();
    };
    const options = {
      sampleRate: 16000, // default 44100
      channels: 1, // 1 or 2, default 1
      bitsPerSample: 16, // 8 or 16, default 16
      audioSource: 6, // android only (see below)
      wavFile: 'test.wav', // default 'audio.wav'
    };

    AudioRecord.init(options);

    console.log('use effect home');
    console.log('use effect home');
  }, [navigation, theme.colors.headerTitle]);

  const getData = async () => {
    try {
      const jsonValue = await AsyncStorage.getItem('@offer_search');
      const searchData = JSON.parse(jsonValue);
      setListData(searchData);
      Tts.speak(searchData.msg, {
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: 0.5,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        },
      });
      Tts.speak(searchData.listOffers[0].item_name, {
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: 0.5,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        },
      });
      const myNumber = searchData.listOffers[0].item_offer_price;
      var myString = myNumber.toString();
      Tts.speak(myString, {
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: 0.5,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        },
      });
    } catch (e) {
      console.log('ee');
      // error reading value
    }
  };
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
    console.log('audioFile 🍷🍷', audioFile);
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
    console.log('upload 🧑‍🚀', fileUrl);
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
      // .then((response) => response.json())
      .then((response) => {
        console.log('response 🔥', response.flag);
        console.log(response);
        if (!response.flag != 'navigation-error') {
          navigation.navigate(response.flag);
        } else {
          console.log('route error');
        }

        // console.log(JSON.stringify(response));
      })
      .catch((err) => console.error(err));
  };

  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
        }}>
        <View
          style={{
            flex: 1,
            flexDirection: 'column',
            justifyContent: 'space-around',
          }}>
          <View
            style={{
              backgroundColor: '#e1e1e1e1',
              width: metrics.screenWidth * 0.95,
              height: '60%',
              borderRadius: 10,
            }}>
            <View
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                flexDirection: 'row',
              }}>
              <Text style={{fontSize: 14, textAlign: 'center', padding: 10}}>
                item name: {resList ? <Text accessible={true} accessibilityLabel={resList.listOffers[0].item_name} accessibilityRole="text">{resList.listOffers[0].item_name}</Text> : null}
              </Text>
              <Text style={{fontSize: 14, textAlign: 'center', padding: 10}}>
                item offer price:
                {resList ? <Text accessible={true} accessibilityLabel={resList.listOffers[0].item_offer_price} accessibilityRole="text">{resList.listOffers[0].item_offer_price}</Text> : null}
              </Text>
            </View>
            <View
              style={{
                display: 'flex',
                flexDirection: 'row',
                justifyContent: 'space-between',
              }}>
              <Text style={{fontSize: 14, textAlign: 'center', padding: 10}}>
                Item price:{resList ? resList.listOffers[0].item_price : null}
              </Text>
              <Text style={{fontSize: 14, textAlign: 'center', padding: 10}}>
                Item stock:{resList ? resList.listOffers[0].item_stock : null}
              </Text>
            </View>
            <View
              style={{
                display: 'flex',
                flexDirection: 'row',
                justifyContent: 'flex-start',
              }}>
              <Text style={{fontSize: 14, textAlign: 'center', padding: 10}}>
                Item unit:{resList ? resList.listOffers[0].item_unit : null}
              </Text>
            </View>

            <ButtonX 
              dark={true}
              color={theme.colors.primary}
              label={'Apply'}
              accessible={true}
              accessibilityLabel=""
              accessibilityHint=""
              accessibilityRole="button"/>
          </View>
        </View>

        <View style={{alignItems: 'center'}}>
          <TouchableOpacity
            onPress={record}
            accessible={true}
            accessibilityLabel="Tap me to Speak"
            accessibilityHint="Start talking to Select an Option"
            accessibilityRole="button"
            >
            <View
              style={{
                padding: 10,
                marginTop: 20,
                backgroundColor: theme.colors.primary,
                borderRadius: 10,
              }}>
              <IconX name={'md-mic'} style={{color: '#fff'}} />
            </View>
          </TouchableOpacity>
        </View>
      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;
