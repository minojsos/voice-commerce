import { React, useContext } from 'react';
import {createStackNavigator} from '@react-navigation/stack';
import BottomTabStack from './BottomStack';
import Routes from '../Routes';
import MenuSelection from '../../Screens/MenuSelection/index';
import LightNowAssistant from '../../Screens/LightNowAssistant/index';
import OrderDetails from '../../Screens/OrderDetails/index';
import OFFERSANDCOUPONS from '../../Screens/OffersAndCo/index';
import OffersNearMe from '../../Screens/OffersNearMe/index';
import PendingDeliveryList from '../../Screens/PendingDeliveryList/index';
import CancelledOrdersList from '../../Screens/CancelledOrdersList/index';
import CompletedOrdersList from '../../Screens/CompletedOrdersList/index';
import CancelledOrder from '../../Screens/CancelledOrder/index';
import CompletedOrder from '../../Screens/CompletedOrder/index';
import PendingDelivery from '../../Screens/PendingDelivery/index';
import ProductSearch from '../../Screens/ProductSearch/index';
import ProductList from '../../Screens/ProductList/index';
import ImageSearch from '../../Screens/ImageSearch/index';
import ImageSearchResult from '../../Screens/PlaceOrder/index';
import Profile from '../../Screens/Profile/index';
import PlaceOrder from '../../Screens/PlaceOrder/index';
import OrderConfirmVoice from '../../Screens/OrderConfirmVoice/index';
import VoiceSearch from '../../Screens/VoiceSearch/index';
import ProductListVoice from '../../Screens/ProductListVoice/index';
import MarkReceived from '../../Screens/MarkReceived/index';
import MarkCancelled from '../../Screens/MarkCancelled/index';
import MarkReturned from '../../Screens/MarkReturned/index';
import Coupons from '../../Screens/Coupons/index';
import VoiceSearchList from '../../Screens/VoiceSearchList/index';
import OrderPharma from '../../Screens/OrderPharma/index';
import VoiceSearchResult from '../../Screens/VoiceSearchResult/index';
import OrderConfirm from '../../Screens/OrderConfirm/index';
import OrderSuccess from '../../Screens/OrderSuccess/index';
import OrderAvailability from '../../Screens/OrderAvailability/index';
import VoiceSearchAlter from '../../Screens/VoiceSearchAlter/index';
import {LocalizationContext} from '../../Translations';

const Stack = createStackNavigator();

const {
  translations,
  appLanguage,
  setAppLanguage,
  initializeAppLanguage,
} = useContext(LocalizationContext); // 1

export default (props) => {
  return (
    <Stack.Navigator headerMode="screen">
      <Stack.Screen
        name={Routes.HOME_TABS}
        options={{headerShown: false}}
        component={BottomTabStack}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['startShoppingTitle']}
        accessibilityRole="text"
        options={{title: translations['startShoppingTitle']}}
        name="language-success"
        component={MenuSelection}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['lightNowAssistantTitle']}
        accessibilityRole="text"
        options={{title: translations['lightNowAssistantTitle']}}
        name="assistant"
        component={LightNowAssistant}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['ordersTitle']}
        accessibilityRole="text"
        options={{title: translations['ordersTitle']}}
        name="orderMenu"
        component={OrderDetails}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['offersAndCouponsTitle']}
        accessibilityRole="text"
        options={{title: translations['offersAndCouponsTitle']}}
        name="list-offer-success"
        component={OFFERSANDCOUPONS}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['couponsTitle']}
        accessibilityRole="text"
        options={{title: translations['couponsTitle']}}
        name="allCoupons"
        component={Coupons}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['offersNearMeTitle']}
        accessibilityRole="text"
        options={{title: translations['offersNearMeTitle']}}
        name="allOffers"
        component={OffersNearMe}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['allPendingOrdersTitle']}
        accessibilityRole="text"
        options={{title: translations['allPendingOrdersTitle']}}
        name="PendingOrdersList"
        component={PendingDeliveryList}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['allCancelledOrdersTitle']}
        accessibilityRole="text"
        options={{title: translations['allCancelledOrdersTitle']}}
        name="cancelledOrdersList"
        component={CancelledOrdersList}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['allCompletedOrdersTitle']}
        accessibilityRole="text"
        options={{title: translations['allCompletedOrdersTitle']}}
        name="completedOrdersList"
        component={CompletedOrdersList}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['cancelledOrderTitle']}
        accessibilityRole="text"
        options={{title: translations['cancelledOrderTitle']}}
        name="orderCancelled"
        component={CancelledOrder}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['completedOrderTitle']}
        accessibilityRole="text"
        options={{title: translations['completedOrderTitle']}}
        name="orderCompleted"
        component={CompletedOrder}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['markReceivedTitle']}
        accessibilityRole="text"
        options={{title: translations['markReceivedTitle']}}
        name="markReceived"
        component={MarkReceived}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['markCancelledTitle']}
        accessibilityRole="text"
        options={{title: translations['markCancelledTitle']}}
        name="markCancelled"
        component={MarkCancelled}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['markReturnedTitle']}
        accessibilityRole="text"
        options={{title: translations['markReturnedTitle']}}
        name="markReturned"
        component={MarkReturned}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['pendingDeliveryTitle']}
        accessibilityRole="text"
        options={{title: translations['pendingDeliveryTitle']}}
        name="orderPending"
        component={PendingDelivery}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['productSearchTitle']}
        accessibilityRole="text"
        options={{title: translations['productSearchTitle']}}
        name="create-list"
        component={ProductSearch}
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['productFinalizeTitle']}
        accessibilityRole="text"
        options={{title: translations['productFinalizeTitle']}}
        component={ProductList}
        name="ProductList"
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['imageSearchTitle']}
        accessibilityRole="text"
        options={{title: translations['imageSearchTitle']}}
        component={ImageSearch}
        name="imageSearch"
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['imageSearchResultTitle']}
        accessibilityRole="text"
        options={{title: translations['imageSearchResultTitle']}}
        component={ImageSearchResult}
        name="ImageSearchResult"
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['profileTitle']}
        accessibilityRole="text"
        options={{title: translations['profileTitle']}}
        component={Profile}
        name="profile"
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['checkoutTitle']}
        accessibilityRole="text"
        options={{title: translations['checkoutTitle']}}
        component={PlaceOrder}
        name="checkout"
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['confirmOrder']}
        accessibilityRole="text"
        options={{title: translations['confirmOrder']}}
        component={OrderConfirm}
        name="orderConfirm"
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['successfullyPlacedOrderTitle']}
        accessibilityRole="text"
        options={{title: translations['successfullyPlacedOrderTitle']}}
        component={OrderSuccess}
        name="orderSuccess"
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['placeYourOrderTitle']}
        accessibilityRole="text"
        options={{title: translations['placeYourOrderTitle']}}
        component={OrderConfirmVoice}
        name="OrderConfirmVoice"
      />
      <Stack.Screen
        acccessible={true}
        accessibilityLabel={translations['yourListTitle']}
        accessibilityRole="text"
        options={{title: translations['yourListTitle']}}
        component={VoiceSearchList}
        name="voiceSearchList"
      />
      <Stack.Screen
        acccessible={true}
        accessibilityLabel={translations['availabilityNearbyShopsTitle']}
        accessibilityRole="text"
        options={{title: translations['availabilityNearbyShopsTitle']}}
        component={OrderAvailability}
        name="orderAvailability"
      />
      <Stack.Screen
        acccessible={true}
        accessibilityLabel={translations['itemAvailabilityList']}
        accessibilityRole="text"
        options={{title: translations['itemAvailabilityList']}}
        component={VoiceSearchResult}
        name="voiceSearchResults"
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['availableItems']}
        accessibilityRole="text"
        options={{title: translations['availableItems']}}
        component={OrderPharma}
        name="voiceSearchPharma"
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['voiceSearchTitle']}
        accessibilityRole="text"
        options={{title: translations['voiceSearchTitle']}}
        component={VoiceSearch}
        name="voiceSearch"
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['alterListTitle']}
        accessibilityRole="text"
        options={{title: translations['alterListTitle']}}
        component={VoiceSearchAlter}
        name="voiceSearchAlter"
      />
      <Stack.Screen
        accessible={true}
        accessibilityLabel={translations['productListTitle']}
        accessibilityRole="text"
        options={{title: translations['productListTitle']}}
        component={ProductListVoice}
        name="search-save"
      />
    </Stack.Navigator>
  );
};
