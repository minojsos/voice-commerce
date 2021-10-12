/* eslint-disable react-native/no-inline-styles */
import React, {useEffect, useContext, useState} from 'react';
import {View, Text, ScrollView, Alert} from 'react-native';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
import {Container, HeaderButton, InputX} from '../../Components';
import useAppTheme from '../../Themes/Context';
import {IconX, ICON_TYPE} from '../../Icons';
import {useStoreState} from 'easy-peasy';
import Fonts from '../../Themes/Fonts';
import {TouchableOpacity, ListItem} from 'react-native';
import AudioRecord from 'react-native-audio-record';
import {BASE_URL} from '../../Config/index';
import Tts from 'react-native-tts';
import {ButtonX} from '../../Components';
import { Avatar, Button, Card, Title, Paragraph } from 'react-native-paper';
import AsyncStorage from '@react-native-community/async-storage';
import {LocalizationContext} from '../../Translations';
import { Voice } from '@react-native-voice/voice';

const MainScreen = ({routes, route, navigation}) => {
  const {theme} = useAppTheme();
  // eslint-disable-next-line prettier/prettier
  const {username, password} = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));
  const [language, setLanguage] = useState('en');
  const [languageTts, setLanguageTts] = useState('en-IN');
  const [resData, setResData] = useState('');
  const [allItems, setAllItems] = useState(route.params);
  const [availableItems, setAvailableItems] = useState([]);
  const [unavailableItems, setUnavailableItems] = useState([]);
  const [similarItems, setSimilarItems] = useState([]);
  const [isRecording, setIsRecording] = useState(false);

  const LISTEN_COMMAND_EN = "begin"
  const LISTEN_COMMAND_TA = "தொடங்க"

  const {
    translations
  } = useContext(LocalizationContext);

  useEffect(() => {
    const _toggleDrawer = () => {
      navigation.toggleDrawer();
    };
    
    Voice.onSpeechStart = onSpeechStart()
    Voice.onSpeechRecognized = onSpeechRecognized()
    Voice.onSpeechResults = onSpeechResults()

    // Iterate and Filter available, unavailable and add similar items
    if (allItems.items.length == 0) {
      // Take user back to Voice Search
      navigation.navigate('voiceSearch')
    }

    var available=[]
    var unavailable=[]
    for (var i=0; i < allItems.items.length; i++) {
      if (allItems.items[i].availability == 1) {
        available.push(allItems.items[i])
      } else {
        unavailable.push(allItems.items[i])
      }
    }

    setAvailableItems(available)
    setUnavailableItems(unavailable)
    setSimilarItems(allItems.similarItems)

    // Load the Chosen Language
    setLanguage(AsyncStorage.getItem('language'))

    if (language == 'ta') {
      setLanguageTts('ta-IN')
    } else {
      setLanguageTts('en-IN')
    }

    Tts.setDefaultLanguage(languageTts)
    Tts.speak(
      translations['voiceSearchTts'],
      {
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: 0.5,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        },
      },
    );
    
    const options = {
      sampleRate: 16000, // default 44100
      channels: 1, // 1 or 2, default 1
      bitsPerSample: 16, // 8 or 16, default 16
      audioSource: 6, // android only (see below)
      wavFile: 'test.wav', // default 'audio.wav'
    };

    AudioRecord.init(options);

    // Read All Data
    read()

    const interval = setInterval(() => {
      if (!isRecording) {
        // Not Recording username or password
        Voice.stop() // Stop Recording
        Voice.start(locale) // Start Recording Again
      }
    }, 5000);
  
    return () => clearInterval(interval); // This represents the unmount function, in which you need to clear your interval to prevent memory leaks.
  }, [navigation, theme.colors.headerTitle]);

  const onSpeechStart = (e) => {

  }

  const onSpeechRecognized = (e) => {
    
  }

  const onSpeechResults = (e) => {
    if (isRecording == false) {
      if (e.value.includes(LISTEN_COMMAND_EN) || e.value.includes(LISTEN_COMMAND_TA)) {
        setIsRecording(true)
        Voice.start(locale)
      }
    } else {
      // Read the Voice Result
      console.log(e.value)
      var menuitem = e.value;
      if (menuitem.includes("read") || menuitem.includes("படி")) {
        // Read the Results
        read()
      } else if (menuitem.includes("continue") || menuitem.includes("தொடரும்")) {
        // Send All items - Available, Unavailable, Similar, Shop Details
        navigation.navigate('voiceSearchPharma', allItems)
      } else if (menuitem.includes("go back") || menuitem.includes("திரும்பி செல்")) {
        navigation.navigate('language-success');
      }

      setIsRecording(false)
    }
  }

  useEffect(() => {
    if (language == 'ta') {
      setLanguageTts('ta-IN')
    } else {
      setLanguageTts('en-IN')
    }

    AsyncStorage.setItem('language', language);
  }, [language]);

  const record = () => {
    AudioRecord.start();
    timeout;
    let timeout = setTimeout(() => {
      stopRecord();
      console.log('hello');
    }, 12000);
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
  };

  const read = () => {
    // Read Available items
    Tts.speak(translations['availableItemsLabel'])
    if (availableItems.length > 0) {
      for (var i = 0; i < availableItems.length; i++) {

      }
    } else {
      Tts.speak(translations['noAvailableItemsLabel'])
    }

    // Read Unavailable Items
    Tts.speak(translations['unavailableItemsLabel'])
    if (unavailableItems.length > 0) {
      for (var i=0; i < unavailableItems.length; i++) {

      }
    } else {
      Tts.speak(translations['noUnavailableItemsLabel'])
    }

    // Similar Items
    Tts.speak(translations['similarItemsLabel'])
    if (similarItems.length > 0) {
      for (var i=0; i < similarItems.length; i++) {

      }
    } else {
      Tts.speak(translations['noSimilarItemsLabel'])
    }
  }
  const readItem = function (item_id) {

  }

  const selectItem = function (item_id) {

  }

  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
          flex: 1
        }}>

        <ScrollView>
          <Title style={{marginTop: 10}}>{translations['availableItemsLabel']}</Title>
          {availableItems ? availableItems.map((item) => {
          return (
            <Card style={{marginTop: 10, backgroundColor: 'rgba(85, 239, 196,0.05)'}} key={item._id}>
              <Card.Content>
                <View style={{flex: 1, flexDirection: 'row'}}>
                  <View style={{
                        flexGrow: 0.1,
                        justifyContent: 'center'
                    }}>
                      <IconX
                        style={{margin: 5}}
                        origin={ICON_TYPE.FONT_AWESOME}
                        name={'circle-o'}
                        color={theme.colors.primary}
                      />
                  </View>
                  <View Style={{
                    flexGrow: 0.5,
                    padding: 5
                  }}>
                    <Paragraph style={{textAlign: 'left'}}>
                      <Text style={{fontSize: 16, textTransform: 'capitalize'}} accessibile={true} accessibilityLabel={item.item_name} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty}  ${item.item_unit}`} accessibilityRole="text">
                        {item.item_name}{"\n"}
                      </Text>
                      <Text style={{fontSize: 12}}>
                        {item.item_qty}{item.item_unit}
                      </Text>
                    </Paragraph>
                  </View>
                  <View style={{
                    flexGrow: 0.2,
                    padding: 5
                  }}>
                    <Paragraph style={{textAlign: 'center'}}>
                      {item.item_offer_price != null ?
                      <>
                      <Text accessibile={true} accessibilityLabel={`${item.item_qty}`} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty} ${item.item_unit}`}>
                        {translations['currencyLabel']}.{item.item_offer_price}/{item.item_unit}{"\n"}
                      </Text>
                      <Text style={{fontSize: 10,textDecorationLine: 'line-through', textDecorationStyle: 'solid'}} accessible={true} accessibilityLabel={`Original Price of ${item.item_name} is ${translations['currencyLabel']}.${item.item_price} and the Offer Price is ${translations['currencyLabel']}.${item.item_offer_price}`}>
                        {translations['currencyLabel']}.{item.item_price}/{item.item_unit}
                      </Text>
                      </>
                      : 
                      <Text accessibile={true} accessibilityLabel={`${item.item_qty}`} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty} ${item.item_unit}`}>
                        {translations['currencyLabel']}.{item.item_price}/{item.item_unit}
                      </Text>
                      }
                    </Paragraph>
                    {/* <Paragraph style={{textAlign: 'center'}}>
                      {item.item_offer_price != null ?
                      <Text accessibile={true} accessibilityLabel={`${item.item_qty}`} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty} ${item.item_unit}`}>
                          Rs.{item.item_offer_price}/{item.item_unit} {"\n"}{item.item_qty}{item.item_unit}
                      </Text>
                      : 
                      <Text accessibile={true} accessibilityLabel={`${item.item_qty}`} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty} ${item.item_unit}`}>
                          Rs.{item.item_price}/{item.item_unit} {"\n"}{item.item_qty}{item.item_unit}
                      </Text>
                      }
                    </Paragraph> */}
                  </View>
                </View>
              </Card.Content>
            </Card>
            )}
          ) : 
          <Text style={{fontSize: 14, color: '#e74c3c'}} accessible={true} accessibilityLabel={translations['noAvailableItems']} accessibilityRole="text">
            {translations['noAvailableItems']}
          </Text>}

          <Title style={{marginTop: 10}}>{translations['unavailableItemsLabel']}</Title>
          {unavailableItems ? unavailableItems.map((item) => {
          return (
            <Card style={{marginTop: 10, backgroundColor: 'rgba(255, 118, 117,0.1)'}} key={item._id}>
              <Card.Content>
                <View style={{flex: 1, flexDirection: 'row'}}>
                  <View style={{
                        flexGrow: 0.1,
                        justifyContent: 'center'
                    }}>
                      <IconX
                        style={{margin: 5}}
                        origin={ICON_TYPE.FONT_AWESOME}
                        name={'circle-o'}
                        color={theme.colors.primary}
                      />
                  </View>
                  <View Style={{
                    flexGrow: 0.5,
                    padding: 5
                  }}>
                    <Paragraph style={{textAlign: 'left'}}>
                      <Text style={{fontSize: 16, textTransform: 'capitalize'}} accessibile={true} accessibilityLabel={item.item_name} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty}  ${item.item_unit}`} accessibilityRole="text">
                        {item.item_name}{"\n"}
                      </Text>
                      <Text style={{fontSize: 12}}>
                        {item.item_qty}{item.item_unit}
                      </Text>
                    </Paragraph>
                  </View>
                  <View style={{
                    flexGrow: 0.2,
                    padding: 5
                  }}>
                    <Paragraph style={{textAlign: 'center'}}>
                      {item.item_offer_price != null ?
                      <>
                      <Text accessibile={true} accessibilityLabel={`${item.item_qty}`} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty} ${item.item_unit}`}>
                        {translations['currencyLabel']}.{item.item_offer_price}/{item.item_unit}{"\n"}
                      </Text>
                      <Text style={{fontSize: 10,textDecorationLine: 'line-through', textDecorationStyle: 'solid'}} accessible={true} accessibilityLabel={`Original Price of ${item.item_name} is Rs.${item.item_price} and the Offer Price is Rs.${item.item_offer_price}`}>
                        {translations['currencyLabel']}.{item.item_price}/{item.item_unit}
                      </Text>
                      </>
                      : 
                      <Text accessibile={true} accessibilityLabel={`${item.item_qty}`} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty} ${item.item_unit}`}>
                        {translations['currencyLabel']}.{item.item_price}/{item.item_unit}
                      </Text>
                      }
                    </Paragraph>
                  </View>
                </View>
              </Card.Content>
            </Card>
            )}
          ) : 
          <Text style={{fontSize: 14, color: '#e74c3c'}} accessible={true} accessibilityLabel={translations['noUnavailableItems']} accessibilityRole="text">
            {translations['noUnavailableItems']}
          </Text>}
          
          <Title style={{marginTop: 10}}>{translations['similarItemsLabel']}</Title>
          {similarItems ? similarItems.map((item) => {
            return (<Card style={{marginTop: 10 }} key={item._id}>
                <Card.Content>
                  <Paragraph style={{textAlign:'left'}}>
                    <Text style={{fontSize: 14, fontWeight: '800', textTransform: 'capitalize'}}>
                      {item.item_name}{"\n"}
                    </Text>
                    <Text style={{fontSize: 12, fontWeight: '600'}}>
                      {translations['currencyLabel']}. {item.item_offer_price != null ? item.item_offer_price : item.item_price}
                    </Text>
                  </Paragraph>
                </Card.Content>
              </Card>)
          }) : 
          <Text style={{fontSize: 14, color: '#e74c3c'}} accessible={true} accessibilityLabel={translations['noSuggestions']} accessibilityRole="text">
            {translations['noSuggestions']}
          </Text>}
        </ScrollView>

        <View style={{flexGrow: 1, alignItems: 'center'}}>
          <TouchableOpacity
            style={{width: '100%'}}
            onPress={record}
            accessible={true}
            accessibilityLabel={translations['micLabel']}
            accessibilityHint={translations['micMenuLabel']}
            accessibilityRole="button"
          >
            <View
              style={{
                alignItems: 'center',
                padding: 10,
                marginTop: 20,
                backgroundColor: theme.colors.primary,
                borderRadius: 10,
              }}>
              <IconX name={'md-mic'} style={{color: '#fff'}} />
            </View>
          </TouchableOpacity>
        </View>
        <View style={{flexGrow: 1, alignItems: 'center'}}>
          <ButtonX
            style={{width: '100%'}}
            dark={true}
            color={theme.colors.primary}
            label={translations['btnContinue']}
            onPress = {() => Tts.speak(translations['btnContinueLongPress'])}
            onLongPress={() => navigation.navigate('voiceSearchPharma', allItems)}
            accessibile={true}
            accessibilityLabel="Proceed to View Pharmaceutical Items"
            accessibilityHint="Proceed to View Pharmaceutical Items"
            accessibilityRole="button"
          />
        </View>
      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;
