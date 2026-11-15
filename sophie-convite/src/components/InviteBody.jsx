import Invitation from './Invitation.jsx'
import Gallery from './Gallery.jsx'
import Transformation from './Transformation.jsx'
import Details from './Details.jsx'
import Actions from './Actions.jsx'
import Finale from './Finale.jsx'
import ScratchCards from './ScratchCards.jsx'

export default function InviteBody({ music }) {
  return (
    <>
      <Invitation music={music} />
      <Transformation />
      <Gallery />
      <Details />
      <Actions />
      <ScratchCards />
      <Finale />
    </>
  )
}
