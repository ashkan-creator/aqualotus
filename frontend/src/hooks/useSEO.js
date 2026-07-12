import { Helmet } from 'react-helmet-async'

/**
 * هوک مرکزی SEO
 * @param {title, description, image, url, type, schema} props
 */
export const SEOHead = ({
  title = 'AquaLotus | فروشگاه گیاهان آبزی',
  description = 'خرید آنلاین گیاهان زنده آکواریوم، کود و مکمل، بستر و لوازم جانبی آکواریوم با ارسال به سراسر ایران',
  image = 'https://aqualotus.ir/logo.png',
  url = 'https://aqualotus.ir',
  type = 'website',
  schema = null,
}) => (
  <Helmet>
    <html lang='fa' dir='rtl' />
    <title>{title}</title>
    <meta name='description' content={description} />
    <meta name='robots' content='index, follow' />
    <meta name='author' content='AquaLotus' />
    <link rel='canonical' href={url} />

    {/* Open Graph */}
    <meta property='og:title' content={title} />
    <meta property='og:description' content={description} />
    <meta property='og:image' content={image} />
    <meta property='og:url' content={url} />
    <meta property='og:type' content={type} />
    <meta property='og:site_name' content='AquaLotus' />
    <meta property='og:locale' content='fa_IR' />

    {/* Twitter Cards */}
    <meta name='twitter:card' content='summary_large_image' />
    <meta name='twitter:title' content={title} />
    <meta name='twitter:description' content={description} />
    <meta name='twitter:image' content={image} />

    {/* Schema.org */}
    {schema && (
      <script type='application/ld+json'>
        {JSON.stringify(schema)}
      </script>
    )}
  </Helmet>
)
