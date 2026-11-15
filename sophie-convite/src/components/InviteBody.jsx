import Invitation from './Invitation.jsx'
import Gallery from './Gallery.jsx'
import DressUp from './DressUp.jsx'
import Details from './Details.jsx'
import Actions from './Actions.jsx'
import Finale from './Finale.jsx'
import Footer from './Footer.jsx'
import ScratchCards from './ScratchCards.jsx'

export default function InviteBody({ music }) {
  return (
    <>
      <Invitation music={music} />
      <DressUp />
      <Gallery />
      <Details />
      <Actions />
      <ScratchCards />
      <Finale />
      <Footer />
    </>
  )
}
